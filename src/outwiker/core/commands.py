# -*- coding: utf-8 -*-

"""
Команды для интерфейса
"""

from datetime import datetime
import os.path
import re
import shutil
import logging

import wx

import outwiker.core.exceptions
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.defines import VERSION_FILE_NAME, VERSIONS_LANG
from outwiker.core.events import PreWikiOpenParams, PostWikiOpenParams
from outwiker.core.pagetitletester import PageTitleError, PageTitleWarning
from outwiker.core.system import getOS, getCurrentDir
from outwiker.core.tree import WikiDocument
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.gui.dialogs.overwritedialog import OverwriteDialog
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.gui.polyaction import PolyAction
from outwiker.gui.dateformatdialog import DateFormatDialog
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.gui.testeddialog import TestedFileDialog
from outwiker.utilites.textfile import readTextFile


logger = logging.getLogger('core')


def MessageBox(*args, **kwargs):
    """
    Замена стандартного MessageBox. Перед показом диалога отключает
    приложение от события EVT_ACTIVATE_APP.
    """
    result = Tester.dialogTester.runNext(None)
    if result is not None:
        return result

    wx.GetApp().unbindActivateApp()
    result = wx.MessageBox(*args, **kwargs)
    wx.GetApp().bindActivateApp()

    return result


def testreadonly(func):
    """
    Декоратор для отлавливания исключения
        outwiker.core.exceptions.ReadonlyException
    """
    def readOnlyWrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except outwiker.core.exceptions.ReadonlyException:
            MessageBox(_(u"Page is opened as read-only"),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)

    return readOnlyWrap


@testreadonly
def attachFiles(parent, page, files):
    """
    Прикрепить файлы к странице с диалогом о перезаписи при необходимости
    parent - родительское окно
    page - страница, куда прикрепляем файлы
    """
    if page.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    oldAttachesFull = Attachment(page).attachmentFull
    oldAttaches = [os.path.basename(fname).lower()
                   for fname in oldAttachesFull]

    # Список файлов, которые будут добавлены
    newAttaches = []

    overwriteDialog = OverwriteDialog(parent)

    for fname in files:
        if fname in oldAttachesFull:
            continue

        if os.path.basename(fname).lower() in oldAttaches:
            text = _(u"File '%s' exists already") % (os.path.basename(fname))
            result = overwriteDialog.ShowDialog(text)

            if result == overwriteDialog.ID_SKIP:
                continue
            elif result == wx.ID_CANCEL:
                break

        newAttaches.append(fname)

    try:
        Attachment(page).attach(newAttaches)
    except IOError as e:
        text = _(u'Error copying files\n{0}').format(str(e))
    except shutil.Error as e:
        text = _(u'Error copying files\n{0}').format(str(e))

    overwriteDialog.Destroy()


@testreadonly
def removePage(page):
    assert page is not None

    if page.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    if page.parent is None:
        MessageBox(_(u"You can't remove the root element"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)
        return

    if (MessageBox(_(u'Remove page "{}" and all subpages?\nAll attached files will also be deleted.').format(page.title),
                   _(u"Remove page?"),
                   wx.YES_NO | wx.ICON_QUESTION) == wx.YES):
        try:
            page.remove()
        except IOError:
            MessageBox(_(u"Can't remove page"),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)


def openWikiWithDialog(parent, readonly=False):
    """
    Показать диалог открытия вики и вернуть открытую wiki
    parent -- родительское окно
    """
    wikiroot = None

    with TestedFileDialog(parent,
                          wildcard="__page.opt|__page.opt",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            fullpath = dialog.GetPath()
            path = os.path.dirname(fullpath)
            wikiroot = openWiki(path, readonly)

    return wikiroot


def findPage(application, page_id):
    """
    page_id - subpath of page or page UID.
    """
    if application.wikiroot is None or page_id is None:
        return None

    prefix = u'page://'

    if page_id.startswith(prefix):
        page_id = page_id[len(prefix):]
        return application.pageUidDepot[page_id]
    elif application.wikiroot[page_id] is not None:
        return application.wikiroot[page_id]
    else:
        return application.pageUidDepot[page_id]


def openWiki(path, readonly=False):
    if not os.path.exists(path):
        __canNotLoadWikiMessage(path)
        return

    # Если передан путь до файла настроек (а не до папки с вики),
    # то оставим только папку
    if not os.path.isdir(path):
        path = os.path.split(path)[0]

    def threadFunc(path, readonly):
        try:
            return WikiDocument.load(path, readonly)
        except BaseException as e:
            return e

    preWikiOpenParams = PreWikiOpenParams(path, readonly)
    Application.onPreWikiOpen(Application.selectedPage,
                              preWikiOpenParams)

    runner = LongProcessRunner(threadFunc,
                               Application.mainWindow,
                               _(u"Loading"),
                               _(u"Opening notes tree..."))
    result = runner.run(os.path.realpath(path), readonly)

    success = False
    if isinstance(result, outwiker.core.exceptions.RootFormatError):
        __rootFormatErrorHandle(path, readonly)
    elif isinstance(result, Exception):
        logger.error(result)
        __canNotLoadWikiMessage(path)
    else:
        Application.wikiroot = result
        success = True

    postWikiOpenParams = PostWikiOpenParams(path, readonly, success)
    Application.onPostWikiOpen(Application.selectedPage,
                               postWikiOpenParams)

    return Application.wikiroot


def __rootFormatErrorHandle(path, readonly):
    """
    Обработчик исключения outwiker.core.exceptions.RootFormatError
    """
    if readonly:
        # Если вики открыт только для чтения, то нельзя изменять файлы
        __canNotLoadWikiMessage(path)
        return

    if (__wantClearWikiOptions(path) != wx.YES):
        return

    # Обнулим файл __page.opt
    WikiDocument.clearConfigFile(path)

    # Попробуем открыть вики еще раз
    try:
        # Загрузить вики
        wikiroot = WikiDocument.load(os.path.realpath(path), readonly)
        Application.wikiroot = wikiroot
    except IOError:
        __canNotLoadWikiMessage(path)

    except outwiker.core.exceptions.RootFormatError:
        __canNotLoadWikiMessage(path)

    finally:
        pass


def __canNotLoadWikiMessage(path):
    """
    Вывести сообщение о том, что невоможно открыть вики
    """
    MessageBox(_(u"Can't load wiki '%s'") % path,
               _(u"Error"),
               wx.ICON_ERROR | wx.OK)


def __wantClearWikiOptions(path):
    """
    Сообщение о том, хочет ли пользователь сбросить файл __page.opt
    """
    return MessageBox(_(u"Can't load wiki '%s'\nFile __page.opt is invalid.\nClear this file and load wiki?\nBookmarks will be lost") % path,
                      _(u"__page.opt error"),
                      wx.ICON_ERROR | wx.YES_NO)


def createNewWiki(parentwnd):
    """
    Создать новую вики
    parentwnd - окно-владелец диалога выбора файла
    """
    dlg = TestedFileDialog(parentwnd, style=wx.FD_SAVE)

    newPageTitle = _(u"First Wiki Page")
    newPageContent = _(u"""!! First Wiki Page

This is the first page. You can use a text formatting: '''bold''', ''italic'', {+underlined text+}, [[https://jenyay.net | link]] and others.""")

    if dlg.ShowModal() == wx.ID_OK:
        try:
            from outwiker.pages.wiki.wikipage import WikiPageFactory

            newwiki = WikiDocument.create(dlg.GetPath())
            WikiPageFactory().create(newwiki, newPageTitle, [_(u"test")])
            firstPage = newwiki[newPageTitle]
            firstPage.content = newPageContent

            Application.wikiroot = newwiki
            Application.wikiroot.selectedPage = firstPage
        except (IOError, OSError) as e:
            # TODO: проверить под Windows
            MessageBox(_(u"Can't create wiki\n") + e.filename,
                       _(u"Error"), wx.OK | wx.ICON_ERROR)

    dlg.Destroy()


def copyTextToClipboard(text):
    if not wx.TheClipboard.Open():
        MessageBox(_(u"Can't open clipboard"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)
        return

    data = wx.TextDataObject(text)

    if not wx.TheClipboard.SetData(data):
        MessageBox(_(u"Can't copy text to clipboard"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)

    wx.TheClipboard.Flush()
    wx.TheClipboard.Close()


def getClipboardText():
    if not wx.TheClipboard.Open():
        MessageBox(_(u"Can't open clipboard"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)
        return

    data = wx.TextDataObject()
    getDataResult = wx.TheClipboard.GetData(data)

    wx.TheClipboard.Close()

    if not getDataResult:
        return

    return data.GetText()


def copyPathToClipboard(page):
    """
    Копировать путь до страницы в буфер обмена
    """
    assert page is not None
    copyTextToClipboard(page.path)


# TODO: Сделать тест
def copyAttachPathToClipboard(page):
    """
    Копировать путь до папки с прикрепленными файлами в буфер обмена
    """
    assert page is not None
    copyTextToClipboard(Attachment(page).getAttachPath(create=True))


@testreadonly
def generateLink(application, page):
    """
    Создать ссылку на страницу по UID
    """
    uid = application.pageUidDepot.createUid(page)
    return u"page://{}".format(uid)


def copyLinkToClipboard(page):
    """
    Копировать ссылку на страницу в буфер обмена
    """
    assert page is not None

    link = generateLink(Application, page)
    if link is not None:
        copyTextToClipboard(link)


def copyTitleToClipboard(page):
    """
    Копировать заголовок страницы в буфер обмена
    """
    assert page is not None
    copyTextToClipboard(page.display_title)


@testreadonly
def movePage(page, newParent):
    """
    Сделать страницу page ребенком newParent
    """
    assert page is not None
    assert newParent is not None

    try:
        page.moveTo(newParent)
    except outwiker.core.exceptions.DuplicateTitle:
        # Невозможно переместить из-за дублирования имен
        MessageBox(_(u"Can't move page when page with that title already exists"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)

    except outwiker.core.exceptions.TreeException:
        # Невозможно переместить по другой причине
        MessageBox(_(u"Can't move page"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)


def setStatusText(text, index=0):
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    Application.mainWindow.statusbar.SetStatusText(text, index)


def getCurrentVersion():
    path = os.path.join(getCurrentDir(), VERSION_FILE_NAME)

    try:
        text = readTextFile(path)
        versionInfo = XmlVersionParser([_(VERSIONS_LANG), u'en']).parse(text)
    except EnvironmentError:
        return None

    return versionInfo.currentVersion


@testreadonly
def renamePage(page, newtitle):
    if page.parent is None:
        MessageBox(_(u"You can't rename the root element"),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)
        return

    newtitle = newtitle.strip()

    if newtitle == page.display_title:
        return

    siblings = [child.title
                for child in page.parent.children
                if child != page]

    real_title = getAlternativeTitle(newtitle, siblings)

    try:
        page.title = real_title
    except OSError:
        MessageBox(_(u'Can\'t rename page "{}" to "{}"').format(page.title, newtitle),
                   _(u"Error"),
                   wx.ICON_ERROR | wx.OK)

    if real_title != newtitle:
        page.alias = newtitle
    else:
        page.alias = None


def testPageTitle(title):
    """
    Возвращает True, если можно создавать страницу с таким заголовком
    """
    tester = getOS().pageTitleTester

    try:
        tester.test(title)

    except PageTitleError as error:
        MessageBox(str(error),
                   _(u"The invalid page title"),
                   wx.OK | wx.ICON_ERROR)
        return False

    except PageTitleWarning as warning:
        text = _(u"{0}\nContinue?").format(str(warning))

        if (MessageBox(text,
                       _(u"The page title"),
                       wx.YES_NO | wx.ICON_QUESTION) == wx.YES):
            return True
        else:
            return False

    return True


def pageExists(page):
    """
    Проверка на то, что страница была удалена сторонними средствами
    """
    return page is not None and os.path.exists(page.path)


def closeWiki(application):
    application.wikiroot = None


def getMainWindowTitle(application):
    template = application.mainWindow.mainWindowConfig.titleFormat.value

    if application.wikiroot is None:
        result = u"OutWiker"
    else:
        page = application.wikiroot.selectedPage

        pageTitle = u"" if page is None else page.display_title
        subpath = u"" if page is None else page.display_subpath
        filename = os.path.basename(application.wikiroot.path)

        result = (template
                  .replace("{file}", filename)
                  .replace("{page}", pageTitle)
                  .replace("{subpath}", subpath)
                  )

    return result


def insertCurrentDate(parent, editor):
    """
    Вызвать диалог для выбора формата даты и вставить в редактор текущую дату согласно выбранному формату.

    parent - родительское окно для диалога
    editor - текстовое поле ввода, куда надо вставить дату (экземпляр класса TextEditor)
    """
    config = GeneralGuiConfig(Application.config)
    initial = config.recentDateTimeFormat.value

    with DateFormatDialog(parent,
                          _(u"Enter format of the date"),
                          _(u"Date format"),
                          initial) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            dateStr = datetime.now().strftime(dlg.Value)
            editor.replaceText(dateStr)
            config.recentDateTimeFormat.value = dlg.Value


def isImage(fname):
    """
    If fname is image then the function return True. Otherwise - False.
    """
    fnameLower = fname.lower()

    return (fnameLower.endswith(".png") or
            fnameLower.endswith(".jpg") or
            fnameLower.endswith(".jpeg") or
            fnameLower.endswith(".bmp") or
            fnameLower.endswith(".gif"))


def dictToStr(paramsDict):
    """
    Return string like param_1="value1" param_2='value "" with double quotes'...
    """
    items = []
    for name, value in paramsDict.items():
        valueStr = str(value)

        hasSingleQuote = u"'" in valueStr
        hasDoubleQuote = u'"' in valueStr

        if hasSingleQuote and hasDoubleQuote:
            valueStr = valueStr.replace(u'"', u'\\"')
            quote = u'"'
        elif hasDoubleQuote:
            quote = u"'"
        else:
            quote = u'"'

        paramStr = u'{name}={quote}{value}{quote}'.format(
            name=name,
            quote=quote,
            value=valueStr
        )

        items.append(paramStr)

    items.sort()
    return u', '.join(items)


def registerActions(application):
    """
    Зарегистрировать действия
    """
    # Действия, связанные с разными типами страниц
    from outwiker.pages.html.htmlpage import HtmlPageFactory
    HtmlPageFactory.registerActions(application)

    from outwiker.pages.wiki.wikipage import WikiPageFactory
    WikiPageFactory.registerActions(application)

    actionController = application.actionController
    from outwiker.gui.actionslist import actionsList, polyactionsList

    # Register the normal actions
    [actionController.register(item[0](application), item[1]) for item in actionsList]

    # Register the polyactions
    [actionController.register(PolyAction(application,
                                          item[0],
                                          item[1],
                                          item[2]),
                               item[3]) for item in polyactionsList]


def getAlternativeTitle(title,
                        siblings,
                        substitution='_',
                        format='{title} ({number})'):
    '''
    The function proposes the page title based on the user title.
    The function replace forbidden characters on the substitution symbol.

    title - original title for the page (with forbidden characters).
    siblings - list of the page titles on the same level.
    substitution - forbidden characters will be replaced to this string.
    format - format string for unique title.

    Return title for the new page.
    '''
    newtitle = title.strip()
    siblings_lower = [sibling.lower().strip() for sibling in siblings]

    # 1. Replace forbidden characters
    regexp = re.compile(r'[><|?*:"\\/#%]')
    newtitle = regexp.sub(substitution, newtitle)

    # 2. Replace double underline in the begin title
    if newtitle.startswith('__'):
        newtitle = '--' + newtitle[2:]

    # 3. Check for special names
    if re.match(r'^\.+$', newtitle):
        newtitle = ''

    # 4. Make unique title
    result = newtitle
    n = 1
    while (len(result.strip()) == 0 or
           result.lower() in siblings_lower):
        result = format.format(title=newtitle, number=n).strip()
        n += 1

    result = result.strip()
    return result

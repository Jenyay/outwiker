#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Команды для интерфейса
"""

import os.path
import shutil

import wx

import outwiker.core.exceptions
from outwiker.core.system import getCurrentDir, getOS
from outwiker.core.version import Version
from outwiker.core.tree import WikiDocument, RootWikiPage
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.pagetitletester import PageTitleError, PageTitleWarning
from outwiker.core.tagscommands import tagBranch, removeTagsFromBranch, renameTag
from outwiker.core.tagslist import TagsList

from outwiker.gui.overwritedialog import OverwriteDialog
from outwiker.gui.about import AboutDialog
from outwiker.gui.tagsdialog import TagsDialog
from outwiker.gui.renametagdialog import RenameTagDialog
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.gui.hotkey import HotKey
from outwiker.gui.polyaction import PolyAction
from outwiker.actions.polyactionsid import *


def MessageBox (*args, **kwargs):
    """
    Замена стандартного MessageBox. Перед показом диалога отключает приложение от события EVT_ACTIVATE_APP.
    """
    wx.GetApp().unbindActivateApp()
    result = wx.MessageBox (*args, **kwargs)
    wx.GetApp().bindActivateApp()

    return result


def testreadonly (func):
    """
    Декоратор для отлавливания исключения outwiker.core.exceptions.ReadonlyException
    """
    def readOnlyWrap (*args, **kwargs):
        try:
            func (*args, **kwargs)
        except outwiker.core.exceptions.ReadonlyException:
            MessageBox (_(u"Wiki is opened as read-only"), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)

    return readOnlyWrap


@testreadonly
def attachFilesWithDialog (parent, page):
    """
    Вызвать диалог для приаттачивания файлов к странице
    parent - родительское окно
    page - страница, куда прикрепляем файлы
    """
    if page.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    dlg = wx.FileDialog (parent, 
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

    if dlg.ShowModal() == wx.ID_OK:
        files = dlg.GetPaths()
        files.sort()
        attachFiles (parent, page, files)

    dlg.Destroy()


@testreadonly
def attachFiles (parent, page, files):
    """
    Прикрепить файлы к странице с диалогом о перезаписи при необходимости
    parent - родительское окно
    page - страница, куда прикрепляем файлы
    """
    if page.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    oldAttaches = [os.path.basename (fname).lower() 
            for fname in Attachment (page).attachmentFull]

    # Список файлов, которые будут добавлены
    newAttaches = []

    overwriteDialog = OverwriteDialog (parent)

    for fname in files:
        if os.path.basename (fname).lower() in oldAttaches:
            text = _(u"File '%s' exists already") % (os.path.basename (fname))
            result = overwriteDialog.ShowDialog (text)

            if result == overwriteDialog.ID_SKIP:
                continue
            elif result == wx.ID_CANCEL:
                break

        newAttaches.append (fname)
    
    try:
        Attachment (page).attach (newAttaches)
    except IOError as e:
        text = _(u'Error copying files\n{0}').format (str (e))
    except shutil.Error as e:
        text = _(u'Error copying files\n{0}').format (str (e))
        
    overwriteDialog.Destroy()


@testreadonly
def removePage (page):
    if page.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    text = _(u"Remove page '%s' and all subpages?") % (page.title)

    if (MessageBox (text, 
        _(u"Remove page?"), 
        wx.YES_NO  | wx.ICON_QUESTION) == wx.YES):
        root = page.root

        try:
            page.remove()
        except IOError:
            MessageBox (_(u"Can't remove page"), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)


def openWikiWithDialog (parent, readonly=False):
    """
    Показать диалог открытия вики и вернуть открытую wiki
    parent -- родительское окно
    """
    wikiroot = None

    dialog = wx.FileDialog (parent, 
            wildcard = "__page.opt|__page.opt", 
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    if dialog.ShowModal() == wx.ID_OK:
        fullpath = dialog.GetPath()
        path = os.path.dirname(fullpath)
        wikiroot = openWiki (path, readonly)

    dialog.Destroy()

    return wikiroot


def openWiki (path, readonly=False):
    wikiroot = None

    Application.onStartTreeUpdate(None)

    def threadFunc (path, readonly):
        try:
            return WikiDocument.load (path, readonly)
        except IOError, error:
            return error
        except outwiker.core.exceptions.RootFormatError, error:
            return error

    runner = LongProcessRunner (threadFunc, 
            Application.mainWindow, 
            _(u"Loading"), 
            _(u"Opening notes tree..."))
    result = runner.run (os.path.realpath (path), readonly)

    if isinstance (result, IOError):
        __canNotLoadWikiMessage (path)
    elif isinstance (result, outwiker.core.exceptions.RootFormatError):
        __rootFormatErrorHandle (path, readonly)
    else:
        Application.wikiroot = result

    Application.onEndTreeUpdate(wikiroot)

    return Application.wikiroot


def __rootFormatErrorHandle (path, readonly):
    """
    Обработчик исключения outwiker.core.exceptions.RootFormatError
    """
    if readonly:
        # Если вики открыт только для чтения, то нельзя изменять файлы
        __canNotLoadWikiMessage (path)
        return

    if (__wantClearWikiOptions (path) != wx.YES):
        return

    # Обнулим файл __page.opt
    WikiDocument.clearConfigFile (path)

    # Попробуем открыть вики еще раз
    try:
        # Загрузить вики
        wikiroot = WikiDocument.load (os.path.realpath (path), readonly)
        Application.wikiroot = wikiroot
    except IOError:
        __canNotLoadWikiMessage (path)

    except outwiker.core.exceptions.RootFormatError:
        __canNotLoadWikiMessage (path)

    finally:
        pass


def __canNotLoadWikiMessage (path):
    """
    Вывести сообщение о том, что невоможно открыть вики
    """
    MessageBox (_(u"Can't load wiki '%s'") % path, 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)


def __wantClearWikiOptions (path):
    """
    Сообщение о том, хочет ли пользователь сбросить файл __page.opt
    """
    return MessageBox (_(u"Can't load wiki '%s'\nFile __page.opt is invalid.\nClear this file and load wiki?\nBookmarks will be lost") % path, 
                _(u"__page.opt error"), 
                wx.ICON_ERROR | wx.YES_NO)


def createNewWiki (parentwnd):
    """
    Создать новую вики
    parentwnd - окно-владелец диалога выбора файла
    """
    dlg = wx.FileDialog (parentwnd, style = wx.FD_SAVE)

    newPageTitle = _(u"First Wiki Page")
    newPageContent = _(u"""!! First Wiki Page

This is the first page. You can use a text formating: '''bold''', ''italic'', {+underlined text+}, [[http://jenyay.net | link]] and others.
""")

    if dlg.ShowModal() == wx.ID_OK:
        try:
            from outwiker.pages.wiki.wikipage import WikiPageFactory

            newwiki = WikiDocument.create (dlg.GetPath ())
            WikiPageFactory.create (newwiki, newPageTitle, [_(u"test")])
            firstPage = newwiki[newPageTitle]
            firstPage.content = newPageContent

            Application.wikiroot = newwiki
            Application.wikiroot.selectedPage = firstPage
        except (IOError, OSError) as e:
            # TODO: проверить под Windows
            MessageBox (_(u"Can't create wiki\n") + unicode (str (e), "utf8"),
                    _(u"Error"), wx.OK | wx.ICON_ERROR)

    dlg.Destroy()


def copyTextToClipboard (text):
    if not wx.TheClipboard.Open():
        MessageBox (_(u"Can't open clipboard"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)
        return

    data = wx.TextDataObject (text)

    if not wx.TheClipboard.SetData(data):
        MessageBox (_(u"Can't copy text to clipboard"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)

    wx.TheClipboard.Flush()
    wx.TheClipboard.Close()


def getClipboardText ():
    if not wx.TheClipboard.Open():
        MessageBox (_(u"Can't open clipboard"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)
        return

    data = wx.TextDataObject()
    getDataResult = wx.TheClipboard.GetData (data)

    wx.TheClipboard.Close()

    if not getDataResult:
        return

    return data.GetText()



def copyPathToClipboard (page):
    """
    Копировать путь до страницы в буфер обмена
    """
    assert page != None
    copyTextToClipboard (page.path)


# TODO: Сделать тест
def copyAttachPathToClipboard (page):
    """
    Копировать путь до папки с прикрепленными файлами в буфер обмена
    """
    assert page != None
    copyTextToClipboard (Attachment(page).getAttachPath(create=True))


def copyLinkToClipboard (page):
    """
    Копировать ссылку на страницу в буфер обмена
    """
    assert page != None
    copyTextToClipboard ("/" + page.subpath)


def copyTitleToClipboard (page):
    """
    Копировать заголовок страницы в буфер обмена
    """
    assert page != None
    copyTextToClipboard (page.title)


@testreadonly
def movePage (page, newParent):
    """
    Сделать страницу page ребенком newParent
    """
    assert page != None
    assert newParent != None

    try:
        page.moveTo (newParent)
    except outwiker.core.exceptions.DublicateTitle:
        # Невозможно переместить из-за дублирования имен
        MessageBox (_(u"Can't move page when page with that title already exists"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)

    except outwiker.core.exceptions.TreeException:
        # Невозможно переместить по другой причине
        MessageBox (_(u"Can't move page"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)


def setStatusText (text, index = 0):
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    Application.mainWindow.statusbar.SetStatusText (text, index)


def getCurrentVersion ():
    fname = "version.txt"
    path = os.path.join (outwiker.core.system.getCurrentDir(), fname)

    try:
        with open (path) as fp:
            lines = fp.readlines()
    except IOError, e:
        MessageBox (_(u"Can't open file %s") % fname, _(u"Error"), wx.ICON_ERROR | wx.OK)
        return

    version_str = "%s.%s %s" % (lines[0].strip(), 
            lines[1].strip(), 
            lines[2].strip())

    try:
        version = Version.parse (version_str)
    except ValueError:
        MessageBox (_(u"Can't parse version"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)
        version = Version(0, 0)

    return version


@testreadonly
def renamePage (page, newtitle):
    if not testPageTitle (newtitle):
        return

    try:
        page.title = newtitle

    except outwiker.core.exceptions.DublicateTitle:
        MessageBox (_(u"Can't move page when page with that title already exists"), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)

    except OSError as e:
        MessageBox (_(u"Can't rename page\n%s") % unicode (e), 
                _(u"Error"), 
                wx.ICON_ERROR | wx.OK)


def showAboutDialog (parent):
    version = getCurrentVersion()
    dlg = AboutDialog (version, parent)
    dlg.ShowModal()
    dlg.Destroy()


def openHelp ():
    help_dir = u"help"
    current_help = _("help_en")
    path = os.path.join (outwiker.core.system.getCurrentDir(), 
            help_dir, 
            current_help)
    openWiki (path, readonly=True)


def reloadWiki (mainWnd):
    """
    Перезагрузить вики
    mainWnd - указатель на главное окно. Нужно, чтобы сообщить ему о необходимости удалить панель с текущей страницей
    """
    if Application.wikiroot != None:
        result = (MessageBox (_(u"Save current page before reload?"), 
            _(u"Save?"), wx.YES_NO | wx.CANCEL  | wx.ICON_QUESTION ))

        if result == wx.CANCEL:
            return

        mainWnd.destroyPagePanel (result == wx.YES)
        openWiki (Application.wikiroot.path)


def testPageTitle (title):
    """
    Возвращает True, если можно создавать страницу с таким заголовком
    """
    tester = getOS().pageTitleTester

    try:
        tester.test (title)

    except PageTitleError as error:
        MessageBox (error.message, 
                _(u"The invalid page title"), 
                wx.OK | wx.ICON_ERROR)
        return False

    except PageTitleWarning as warning:
        text = _(u"{0}\nContinue?").format (warning.message)

        if (MessageBox (text, 
            _(u"The page title"), 
            wx.YES_NO | wx.ICON_QUESTION ) == wx.YES):
            return True
        else:
            return False

    return True


def pageExists (page):
    """
    Проверка на то, что страница была удалена сторонними средствами
    """
    return page != None and os.path.exists (page.path)


@testreadonly
def addTagsToBranchGui (page, parent):
    """
    Добавить теги к ветке, начинающейся со страницы page. 
    Теги к странице page тоже добавляются
    """
    dlg = TagsDialog (parent, Application)
    dlg.SetTitle (_(u"Add Tags to Branch"))

    if dlg.ShowModal() == wx.ID_OK:
        Application.onStartTreeUpdate(page.root)

        try:
            tagBranch (page, dlg.tags)
        finally:
            Application.onEndTreeUpdate(page.root)

    dlg.Destroy()


@testreadonly
def removeTagsFromBranchGui (page, parent):
    """
    Удалить теги из ветки, начинающейся со страницы page
    """
    dlg = TagsDialog (parent, Application)
    dlg.SetTitle (_(u"Remove Tags from Branch"))

    if dlg.ShowModal() == wx.ID_OK:
        Application.onStartTreeUpdate(page.root)

        try:
            removeTagsFromBranch (page, dlg.tags)
        finally:
            Application.onEndTreeUpdate(page.root)

    dlg.Destroy()
        

@testreadonly
def renameTagGui (wikiroot, parent):
    tagslist = TagsList (wikiroot)

    dlg = RenameTagDialog (parent, tagslist)
    if dlg.ShowModal() == wx.ID_OK:
        Application.onStartTreeUpdate(wikiroot)

        try:
            renameTag (wikiroot, dlg.oldTagName, dlg.newTagName)
        finally:
            Application.onEndTreeUpdate(wikiroot)

    dlg.Destroy()


def closeCurrentTab (application):
    """
    Закыть текущую вкладку
    """
    assert application.mainWindow != None

    index = application.mainWindow.tabsController.getSelection()
    if index != -1:
        application.mainWindow.tabsController.closeTab (index)


def addNewTab (application):
    assert application.mainWindow != None
    application.mainWindow.tabsController.cloneTab()


def closeWiki (application):
    application.wikiroot = None


def nextTab (application):
    assert application.mainWindow != None
    tabsCount = application.mainWindow.tabsController.nextTab()


def previousTab (application):
    assert application.mainWindow != None
    tabsCount = application.mainWindow.tabsController.previousTab()


def getMainWindowTitle (application):
    template = application.mainWindow.mainWindowConfig.titleFormat.value

    if application.wikiroot == None:
        result = u"OutWiker"
    else:
        pageTitle = (u"" if application.wikiroot.selectedPage == None 
                else application.wikiroot.selectedPage.title)
        filename = os.path.basename (application.wikiroot.path)

        result = template.replace ("{file}", filename).replace ("{page}", pageTitle)

    return result


def registerActions (application):
    """
    Зарегистрировать действия
    """
    # Действия, связанные с разными типами страниц
    from outwiker.pages.html.htmlpage import HtmlPageFactory
    HtmlPageFactory.registerActions (application)

    from outwiker.pages.wiki.wikipage import WikiPageFactory
    WikiPageFactory.registerActions (application)


    # Открыть...
    from outwiker.actions.open import OpenAction
    application.actionController.register (OpenAction (application), 
            HotKey ("O", ctrl=True))

    # Создать...
    from outwiker.actions.new import NewAction
    application.actionController.register (NewAction (application), 
            HotKey ("N", ctrl=True))

    # Открыть только для чтения
    from outwiker.actions.openreadonly import OpenReadOnlyAction
    application.actionController.register (OpenReadOnlyAction (application), 
            HotKey ("O", ctrl=True, shift=True))
    
    # Закрыть
    from outwiker.actions.close import CloseAction
    application.actionController.register (CloseAction (application), 
            HotKey ("W", ctrl=True, shift=True))

    # Сохранить
    from outwiker.actions.save import SaveAction
    application.actionController.register (SaveAction (application), 
            HotKey ("S", ctrl=True))

    # Печать
    from outwiker.actions.printaction import PrintAction
    application.actionController.register (PrintAction (application), 
            HotKey ("P", ctrl=True))

    # Выход
    from outwiker.actions.exit import ExitAction
    application.actionController.register (ExitAction (application), 
            HotKey ("F4", alt=True))

    # Показать / скрыть панель с прикрепленными файлами
    from outwiker.actions.showhideattaches import ShowHideAttachesAction
    application.actionController.register (ShowHideAttachesAction (application))

    # Показать / скрыть панель с деревом заметок
    from outwiker.actions.showhidetree import ShowHideTreeAction
    application.actionController.register (ShowHideTreeAction (application))

    # Показать / скрыть панель с тегами
    from outwiker.actions.showhidetags import ShowHideTagsAction
    application.actionController.register (ShowHideTagsAction (application))

    # Полноэкранный режим
    from outwiker.actions.fullscreen import FullScreenAction
    application.actionController.register (FullScreenAction (application), 
            HotKey ("F11") )

    # Поиск
    from outwiker.actions.search import SearchAction, SearchNextAction, SearchPrevAction
    application.actionController.register (SearchAction (application), 
            HotKey ("F", ctrl=True) )

    application.actionController.register (SearchNextAction (application), 
            HotKey ("F3") )

    application.actionController.register (SearchPrevAction (application), 
            HotKey ("F3", shift=True) )


    # Вызов настроек
    from outwiker.actions.preferences import PreferencesAction
    application.actionController.register (PreferencesAction (application), 
            HotKey ("F8", ctrl=True) )


    # Добавить страницу того же уровня
    from outwiker.actions.addsiblingpage import AddSiblingPageAction
    application.actionController.register (AddSiblingPageAction (application), 
            HotKey ("T", ctrl=True, alt=True) )


    # Добавить дочернюю страницу
    from outwiker.actions.addchildpage import AddChildPageAction
    application.actionController.register (AddChildPageAction (application), 
            HotKey ("T", ctrl=True, shift=True) )


    # Переместить страницу на одну позицию вверх
    from outwiker.actions.movepageup import MovePageUpAction
    application.actionController.register (MovePageUpAction (application), 
            HotKey ("Up", ctrl=True, shift=True) )


    # Переместить страницу на одну позицию вниз
    from outwiker.actions.movepagedown import MovePageDownAction
    application.actionController.register (MovePageDownAction (application), 
            HotKey ("Down", ctrl=True, shift=True) )

    # Сортировка дочерних страниц по алфавиту
    from outwiker.actions.sortchildalpha import SortChildAlphabeticalAction
    application.actionController.register (SortChildAlphabeticalAction (application), 
            None)


    # Сортировка страниц того же уровня, что и выбранная, по алфавиту
    from outwiker.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
    application.actionController.register (SortSiblingsAlphabeticalAction (application), 
            None)


    # Переименование текущей страницы
    from outwiker.actions.renamepage import RenamePageAction
    application.actionController.register (RenamePageAction (application), 
            HotKey ("F2"))


    # Удаление текущей страницы
    from outwiker.actions.removepage import RemovePageAction
    application.actionController.register (RemovePageAction (application), 
            HotKey ("Delete", ctrl=True, shift=True))


    # Редактирование свойств страницы
    from outwiker.actions.editpageprop import EditPagePropertiesAction
    application.actionController.register (EditPagePropertiesAction (application), 
            HotKey ("E", ctrl=True))

    _registerPolyActions (application)


def _registerPolyActions (application):
    # Шрифты

    application.actionController.register (PolyAction (application,
        BOLD_STR_ID,
        _(u"Bold"),
        _(u"Bold")),
        HotKey ("B", ctrl=True))

    application.actionController.register (PolyAction (application,
        ITALIC_STR_ID,
        _(u"Italic"),
        _(u"Italic")),
        HotKey ("I", ctrl=True))

    application.actionController.register (PolyAction (application,
        BOLD_ITALIC_STR_ID,
        _(u"Bold italic"),
        _(u"Bold italic")),
        HotKey ("I", ctrl=True, shift=True))

    application.actionController.register (PolyAction (application,
        UNDERLINE_STR_ID,
        _(u"Underline"),
        _(u"Underline")),
        HotKey ("U", ctrl=True))

    application.actionController.register (PolyAction (application,
        STRIKE_STR_ID,
        _(u"Strikethrough"),
        _(u"Strikethrough")),
        HotKey ("K", ctrl=True))

    application.actionController.register (PolyAction (application,
        SUBSCRIPT_STR_ID,
        _(u"Subscript"),
        _(u"Subscript")),
        HotKey ("=", ctrl=True))

    application.actionController.register (PolyAction (application,
        SUPERSCRIPT_STR_ID,
        _(u"Superscript"),
        _(u"Superscript")),
        HotKey ("+", ctrl=True))

    application.actionController.register (PolyAction (application,
        PREFORMAT_STR_ID,
        _(u"Preformatted text"),
        _(u"Preformatted text")),
        HotKey ("F", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        CODE_STR_ID,
        _(u"Insert code"),
        _(u"Insert code (monospaced font)")),
        HotKey ("D", ctrl=True, alt=True))


    # Выравнивания

    application.actionController.register (PolyAction (application,
        ALIGN_LEFT_STR_ID,
        _(u"Align text left"),
        _(u"Align text left")),
        HotKey ("L", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        ALIGN_CENTER_STR_ID,
        _(u"Center"),
        _(u"Center")),
        HotKey ("C", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        ALIGN_RIGHT_STR_ID,
        _(u"Align text right"),
        _(u"Align text right")),
        HotKey ("R", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        ALIGN_JUSTIFY_STR_ID,
        _(u"Justify"),
        _(u"Justify")),
        HotKey ("J", ctrl=True, alt=True))


    # Заголовки
    application.actionController.register (PolyAction (application,
        HEADING_1_STR_ID,
        _(u"First-level heading"),
        _(u"First-level heading")),
        HotKey ("1", ctrl=True))

    application.actionController.register (PolyAction (application,
        HEADING_2_STR_ID,
        _(u"Second-level heading"),
        _(u"Second-level heading")),
        HotKey ("2", ctrl=True))

    application.actionController.register (PolyAction (application,
        HEADING_3_STR_ID,
        _(u"Subtitle three"),
        _(u"Subtitle three")),
        HotKey ("3", ctrl=True))

    application.actionController.register (PolyAction (application,
        HEADING_4_STR_ID,
        _(u"Subtitle four"),
        _(u"Subtitle four")),
        HotKey ("4", ctrl=True))

    application.actionController.register (PolyAction (application,
        HEADING_5_STR_ID,
        _(u"Subtitle five"),
        _(u"Subtitle five")),
        HotKey ("5", ctrl=True))

    application.actionController.register (PolyAction (application,
        HEADING_6_STR_ID,
        _(u"Subtitle six"),
        _(u"Subtitle six")),
        HotKey ("6", ctrl=True))

    # Разное
    application.actionController.register (PolyAction (application,
        ANCHOR_STR_ID,
        _(u"Anchor"),
        _(u"Anchor")),
        HotKey ("N", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        HORLINE_STR_ID,
        _(u"Horizontal rule"),
        _(u"Horizontal rule")),
        HotKey ("H", ctrl=True))

    application.actionController.register (PolyAction (application,
        LINK_STR_ID,
        _(u"Link"),
        _(u"Insert Link")),
        HotKey ("L", ctrl=True))

    application.actionController.register (PolyAction (application,
        QUOTE_STR_ID,
        _(u"Quote"),
        _(u"Insert a quote block")),
        HotKey ("Q", ctrl=True, alt=True))

    application.actionController.register (PolyAction (application,
        IMAGE_STR_ID,
        _(u"Image"),
        _(u"Insert image")),
        HotKey ("M", ctrl=True))


    # Списки
    application.actionController.register (PolyAction (application,
        LIST_BULLETS_STR_ID,
        _(u"Bullets list"),
        _(u"Insert a bullets list")),
        HotKey ("G", ctrl=True))

    application.actionController.register (PolyAction (application,
        LIST_NUMBERS_STR_ID,
        _(u"Numbers list"),
        _(u"Insert a numbers list")),
        HotKey ("J", ctrl=True))

    application.actionController.register (PolyAction (application,
        LINE_BREAK_STR_ID,
        _(u"Line break"),
        _(u"Insert a line break")),
        HotKey ("Return", ctrl=True))

    application.actionController.register (PolyAction (application,
        HTML_ESCAPE_STR_ID,
        _(u"Convert HTML Symbols"),
        _(u"Convert HTML Symbols")),
        None)


    # Таблицы
    application.actionController.register (PolyAction (application,
        TABLE_STR_ID,
        _(u"Table"),
        _(u"Insert a table")),
        HotKey ("Q", ctrl=True))

    application.actionController.register (PolyAction (application,
        TABLE_ROW_STR_ID,
        _(u"Table row"),
        _(u"Insert a table row")),
        HotKey ("W", ctrl=True))

    application.actionController.register (PolyAction (application,
        TABLE_CELL_STR_ID,
        _(u"Table cell"),
        _(u"Insert a table cell")),
        HotKey ("Y", ctrl=True))

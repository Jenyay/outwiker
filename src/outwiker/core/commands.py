# -*- coding: utf-8 -*-

"""
Команды для интерфейса
"""

import logging
import os
import os.path
from datetime import datetime
from typing import Optional

import wx

import outwiker.core.exceptions
from outwiker.api.services.messages import showError
from outwiker.core.application import Application
from outwiker.core.pagetitletester import PageTitleError, PageTitleWarning
from outwiker.core.system import getOS
from outwiker.core.tree import WikiDocument
from outwiker.core.tree_commands import getAlternativeTitle
from outwiker.gui.dateformatdialog import DateFormatDialog
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.testeddialog import TestedFileDialog

# TODO: Remove in next version
from outwiker.api.core.images import isImage
from outwiker.api.core.tree import testreadonly
from outwiker.api.services.attachment import attachFiles
from outwiker.api.services.clipboard import copyTextToClipboard
from outwiker.api.services.tree import openWiki
from outwiker.api.gui.dialogs.messagebox import MessageBox


logger = logging.getLogger('outwiker.core.commands')


def findPage(application, page_id):
    """
    page_id - subpath of page or page UID.
    """
    if application.wikiroot is None or page_id is None:
        return None

    prefix = 'page://'

    if page_id.startswith(prefix):
        page_id = page_id[len(prefix):]
        return application.pageUidDepot[page_id]
    elif application.wikiroot[page_id] is not None:
        return application.wikiroot[page_id]
    else:
        return application.pageUidDepot[page_id]


def createNewWiki(parentwnd):
    """
    Создать новую вики
    parentwnd - окно-владелец диалога выбора файла
    """
    newPageTitle = _("First Wiki Page")
    newPageContent = _("""!! First Wiki Page

This is the first page. You can use a text formatting: '''bold''', ''italic'', {+underlined text+}, [[https://jenyay.net | link]] and others.""")

    with TestedFileDialog(parentwnd, style=wx.FD_SAVE) as dlg:
        dlg.SetDirectory(getOS().documentsDir)

        if dlg.ShowModal() == wx.ID_OK:
            try:
                from outwiker.pages.wiki.wikipage import WikiPageFactory

                newwiki = WikiDocument.create(dlg.GetPath())
                WikiPageFactory().create(newwiki, newPageTitle, [_("test")])
                firstPage = newwiki[newPageTitle]
                firstPage.content = newPageContent

                Application.wikiroot = newwiki
                Application.wikiroot.selectedPage = firstPage
            except (IOError, OSError) as e:
                # TODO: проверить под Windows
                showError(Application.mainWindow, _(
                    "Can't create wiki\n") + e.filename)


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
        showError(Application.mainWindow, _(
            "Can't move page when page with that title already exists"))
    except outwiker.core.exceptions.TreeException:
        # Невозможно переместить по другой причине
        showError(Application.mainWindow, _(
            "Can't move page: {}".format(page.display_title)))


def addStatusBarItem(name: str, width: int = -1, position: Optional[int] = None) -> None:
    if Application.mainWindow:
        Application.mainWindow.statusbar.addItem(name, width, position)


def setStatusText(item_name: str, text: str) -> None:
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    if Application.mainWindow:
        Application.mainWindow.statusbar.setStatusText(item_name, text)


@testreadonly
def renamePage(page, newtitle):
    if page.parent is None:
        showError(Application.mainWindow, _(
            "You can't rename the root element"))
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
        showError(Application.mainWindow,
                  _('Can\'t rename page "{}" to "{}"').format(page.display_title, newtitle))

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
                   _("Invalid page title"),
                   wx.OK | wx.ICON_ERROR)
        return False

    except PageTitleWarning as warning:
        text = _("{0}\nContinue?").format(str(warning))

        if (MessageBox(text,
                       _("The page title"),
                       wx.YES_NO | wx.ICON_QUESTION) == wx.YES):
            return True
        else:
            return False

    return True


def getMainWindowTitle(application):
    template = application.mainWindow.mainWindowConfig.titleFormat.value

    if application.wikiroot is None:
        result = "OutWiker"
    else:
        page = application.wikiroot.selectedPage

        pageTitle = "" if page is None else page.display_title
        subpath = "" if page is None else page.display_subpath
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
                          _("Enter format of the date"),
                          _("Date format"),
                          initial) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            dateStr = datetime.now().strftime(dlg.Value)
            editor.replaceText(dateStr)
            config.recentDateTimeFormat.value = dlg.Value

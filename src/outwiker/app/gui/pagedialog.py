# -*- coding: utf-8 -*-

from typing import List, Optional

import wx

from outwiker.app.services.messages import showError
from outwiker.app.services.tree import renamePage
from outwiker.app.gui.basepagedialog import BasePageDialog
from outwiker.core.application import Application
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.tree import BasePage, WikiPage
from outwiker.core.treetools import pageExists, testreadonly


@testreadonly
def editPage(parentWnd, currentPage, application):
    """
    Вызвать диалог для редактирования страницы
    parentWnd - родительское окно
    currentPage - страница для редактирования
    """
    if currentPage.readonly:
        raise ReadonlyException

    if not pageExists(currentPage):
        showError(
            application.mainWindow, _('Page "%s" not found') % currentPage.display_title
        )
        return

    with EditPageDialog(parentWnd, currentPage, application) as dlg:
        dlg.generalPanel.setOpenInNewTabVisible(False)
        if dlg.ShowModal() == wx.ID_OK:
            renamePage(currentPage, dlg.pageTitle)
            if not dlg.setPageProperties(currentPage):
                return None


@testreadonly
def createPageWithDialog(
    parentwnd: wx.Window,
    parentpage: BasePage,
    application: Application,
    content: Optional[str] = None,
) -> Optional[WikiPage]:
    """
    Показать диалог настроек и создать страницу
    """
    assert parentpage is not None

    if parentpage.readonly:
        raise ReadonlyException

    page = None

    with CreatePageDialog(parentwnd, parentpage, application) as dlg:
        dlg.generalPanel.setOpenInNewTabVisible(True)
        if dlg.ShowModal() == wx.ID_OK:
            factory = dlg.selectedFactory
            alias = dlg.pageTitle
            order_calculator = dlg.orderCalculator
            tags: List[str] = []

            try:
                page = factory.create(parentpage, alias, tags, order_calculator)
                if content is not None:
                    page.content = content
            except OSError:
                showError(application.mainWindow, _("Can't create page"))
                return None

            assert page is not None
            if not dlg.setPageProperties(page):
                return None

            if dlg.generalPanel.isOpenInNewTab:
                if application.mainWindow is not None:
                    application.mainWindow.tabsController.openInTab(page, True)
            else:
                page.root.selectedPage = page

    return page


def createSiblingPage(parentwnd, page: Optional[WikiPage], application: Application):
    """
    Создать страницу, находящуюся на том же уровне, что и текущая страница
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert application.wikiroot is not None

    selectet_text = None
    if page is None or page.parent is None:
        parentpage = application.wikiroot
    else:
        parentpage = page.parent
        selectet_text = application.selectedText

    createPageWithDialog(parentwnd, parentpage, application, content=selectet_text)


def createChildPage(parentwnd, page: Optional[BasePage], application: Application):
    """
    Создать страницу, которая будет дочерней к текущей странице
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert application.wikiroot is not None

    selectet_text = None
    if page is None:
        page = application.wikiroot
    else:
        selectet_text = application.selectedText

    createPageWithDialog(parentwnd, page, application, content=selectet_text)


class CreatePageDialog(BasePageDialog):
    def __init__(self, parentWnd, parentPage: BasePage, application: Application):
        super().__init__(parentWnd, None, parentPage, application)
        self.SetTitle(_("Create Page"))

    def _validate(self):
        for controller in self._controllers:
            if not controller.validateBeforeCreation(self.parentPage):
                return False

        return True

    def _initController(self, controller):
        controller.initBeforeCreation(self.parentPage)


class EditPageDialog(BasePageDialog):
    def __init__(self, parentWnd, currentPage, application: Application):
        assert currentPage is not None

        super().__init__(parentWnd, currentPage, currentPage.parent, application)

        self.SetTitle(_("Edit page properties"))

    def _initController(self, controller):
        controller.initBeforeEditing(self.currentPage)

    def _validate(self):
        for controller in self._controllers:
            if not controller.validateBeforeEditing(self.currentPage):
                return False

        return True

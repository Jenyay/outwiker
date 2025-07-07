# -*- coding: utf-8 -*-

import wx

from outwiker.app.services.messages import showError
from outwiker.app.services.tree import renamePage
from outwiker.app.gui.basepagedialog import BasePageDialog
from outwiker.core.exceptions import ReadonlyException
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
        showError(application.mainWindow,
                  _('Page "%s" not found') % currentPage.display_title)
        return

    with EditPageDialog(parentWnd, currentPage, application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            renamePage(currentPage, dlg.pageTitle)
            if not dlg.setPageProperties(currentPage):
                return None


@testreadonly
def createPageWithDialog(parentwnd, parentpage, application):
    """
    Показать диалог настроек и создать страницу
    """
    assert parentpage is not None

    if parentpage.readonly:
        raise ReadonlyException

    page = None

    with CreatePageDialog(parentwnd, parentpage, application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            factory = dlg.selectedFactory
            alias = dlg.pageTitle
            order_calculator = dlg.orderCalculator
            tags = []

            try:
                page = factory.create(
                    parentpage, alias, tags, order_calculator)
            except OSError:
                showError(application.mainWindow, _("Can't create page"))
                return None

            assert page is not None
            if not dlg.setPageProperties(page):
                return None

            page.root.selectedPage = page

    return page


def createSiblingPage(parentwnd, page, application):
    """
    Создать страницу, находящуюся на том же уровне, что и текущая страница
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert application.wikiroot is not None

    if page is None or page.parent is None:
        parentpage = application.wikiroot
    else:
        parentpage = page.parent

    createPageWithDialog(parentwnd, parentpage, application)


def createChildPage(parentwnd, page, application):
    """
    Создать страницу, которая будет дочерней к текущей странице
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert application.wikiroot is not None

    if page is None:
        page = application.wikiroot

    createPageWithDialog(parentwnd, page, application)


class CreatePageDialog(BasePageDialog):
    def __init__(self, parentWnd, parentPage, application):
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
    def __init__(self, parentWnd, currentPage, application):
        assert currentPage is not None

        super().__init__(parentWnd, currentPage, currentPage.parent,
                         application)

        self.SetTitle(_("Edit page properties"))

    def _initController(self, controller):
        controller.initBeforeEditing(self.currentPage)

    def _validate(self):
        for controller in self._controllers:
            if not controller.validateBeforeEditing(self.currentPage):
                return False

        return True

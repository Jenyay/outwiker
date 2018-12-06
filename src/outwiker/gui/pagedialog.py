# -*- coding: utf-8 -*-

import wx

import outwiker.core.commands
from .basepagedialog import BasePageDialog
from outwiker.core.application import Application
from outwiker.core.commands import (pageExists,
                                    showError,
                                    getAlternativeTitle,
                                    renamePage)


@outwiker.core.commands.testreadonly
def editPage(parentWnd, currentPage):
    """
    Вызвать диалог для редактирования страницы
    parentWnd - родительское окно
    currentPage - страница для редактирования
    """
    if currentPage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    if not pageExists(currentPage):
        showError(Application.mainWindow,
                  _(u'Page "%s" not found') % currentPage.display_title)
        return

    with EditPageDialog(parentWnd, currentPage, Application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            renamePage(currentPage, dlg.pageTitle)
            if not dlg.setPageProperties(currentPage):
                return None


@outwiker.core.commands.testreadonly
def createPageWithDialog(parentwnd, parentpage):
    """
    Показать диалог настроек и создать страницу
    """
    assert parentpage is not None

    if parentpage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    page = None

    with CreatePageDialog(parentwnd, parentpage, Application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            factory = dlg.selectedFactory
            alias = dlg.pageTitle
            siblings = [child_page.title for child_page in parentpage.children]
            title = getAlternativeTitle(alias, siblings)

            try:
                page = factory.create(parentpage, title, [])
                if title != alias:
                    page.alias = alias
            except EnvironmentError:
                showError(Application.mainWindow, _(u"Can't create page"))
                return None

            assert page is not None
            if not dlg.setPageProperties(page):
                return None

            page.root.selectedPage = page

    return page


def createSiblingPage(parentwnd, page):
    """
    Создать страницу, находящуюся на том же уровне, что и текущая страница
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert Application.wikiroot is not None

    if page is None or page.parent is None:
        parentpage = Application.wikiroot
    else:
        parentpage = page.parent

    createPageWithDialog(parentwnd, parentpage)


def createChildPage(parentwnd, page):
    """
    Создать страницу, которая будет дочерней к текущей странице
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert Application.wikiroot is not None

    if page is None:
        page = Application.wikiroot

    createPageWithDialog(parentwnd, page)


class CreatePageDialog(BasePageDialog):
    def __init__(self, parentWnd, parentPage, application):
        super().__init__(parentWnd, None, parentPage, application)
        self.SetTitle(_(u"Create Page"))

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

        self.SetTitle(_(u"Edit page properties"))

    def _initController(self, controller):
        controller.initBeforeEditing(self.currentPage)

    def _validate(self):
        for controller in self._controllers:
            if not controller.validateBeforeEditing(self.currentPage):
                return False

        return True

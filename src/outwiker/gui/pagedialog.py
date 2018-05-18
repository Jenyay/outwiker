# -*- coding: utf-8 -*-

import wx

import outwiker.core.commands
from .basepagedialog import BasePageDialog
from outwiker.core.application import Application
from outwiker.core.commands import pageExists, MessageBox


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
        MessageBox(_(u'Page "%s" not found') % currentPage.display_title,
                   _(u"Error"),
                   wx.OK | wx.ICON_ERROR)
        return

    with EditPageDialog(parentWnd, currentPage, Application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            try:
                currentPage.display_title = dlg.pageTitle
            except EnvironmentError as e:
                MessageBox(_(u"Can't rename page\n") + str(e),
                           _(u"Error"),
                           wx.ICON_ERROR | wx.OK)

            if not dlg.setPageProperties(currentPage):
                return None


@outwiker.core.commands.testreadonly
def createPageWithDialog(parentwnd, parentpage):
    """
    Показать диалог настроек и создать страницу
    """
    if parentpage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    page = None

    with CreatePageDialog(parentwnd, parentpage, Application) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            factory = dlg.selectedFactory
            title = dlg.pageTitle

            try:
                page = factory.create(parentpage, title, [])
            except EnvironmentError:
                MessageBox(_(u"Can't create page"),
                           "Error",
                           wx.ICON_ERROR | wx.OK)
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

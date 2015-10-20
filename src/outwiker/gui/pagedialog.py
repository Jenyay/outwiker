# -*- coding: utf-8 -*-

import wx

import outwiker.core.commands
from .basepagedialog import BasePageDialog
from outwiker.core.application import Application
from outwiker.core.commands import pageExists, MessageBox


@outwiker.core.commands.testreadonly
def editPage (parentWnd, currentPage):
    """
    Вызвать диалог для редактирования страницы
    parentWnd - родительское окно
    currentPage - страница для редактирования
    """
    if currentPage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    if not pageExists (currentPage):
        MessageBox (_(u'Page "%s" not found') % currentPage.title,
                    _(u"Error"),
                    wx.OK | wx.ICON_ERROR)
        return

    with EditPageDialog (currentPage, parent = parentWnd) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            try:
                currentPage.title = dlg.pageTitle
            except EnvironmentError as e:
                MessageBox (_(u"Can't rename page\n") + unicode (e),
                            _(u"Error"),
                            wx.ICON_ERROR | wx.OK)

            if not dlg.setPageProperties (currentPage):
                return None

            currentPage.root.selectedPage = currentPage


@outwiker.core.commands.testreadonly
def createPageWithDialog (parentwnd, parentpage):
    """
    Показать диалог настроек и создать страницу
    """
    if parentpage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    page = None

    with CreatePageDialog (parentpage, parentwnd) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            factory = dlg.selectedFactory
            title = dlg.pageTitle

            try:
                page = factory.create (parentpage, title, [])
            except EnvironmentError:
                MessageBox (_(u"Can't create page"),
                            "Error",
                            wx.ICON_ERROR | wx.OK)
                return None

            assert page is not None
            if not dlg.setPageProperties (page):
                return None

            page.root.selectedPage = page

    return page


def createSiblingPage (parentwnd, page):
    """
    Создать страницу, находящуюся на том же уровне, что и текущая страница
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert Application.wikiroot is not None

    if page is None or page.parent is None:
        parentpage = Application.wikiroot
    else:
        parentpage = page.parent

    createPageWithDialog (parentwnd, parentpage)


def createChildPage (parentwnd, page):
    """
    Создать страницу, которая будет дочерней к текущей странице
    parentwnd - окно, которое будет родителем для диалога создания страницы
    """
    assert Application.wikiroot is not None

    if page is None:
        page = Application.wikiroot

    createPageWithDialog (parentwnd, page)


class CreatePageDialog (BasePageDialog):
    def __init__ (self, parentPage = None, *args, **kwds):
        super (CreatePageDialog, self).__init__ (*args, **kwds)
        self.SetTitle(_(u"Create Page"))

        self._parentPage = parentPage

        map (lambda panel: panel.initBeforeCreation (self._parentPage),
             self._panels)


    def _validate (self):
        for panel in self._panels:
            if not panel.validateBeforeCreation (self._parentPage):
                return False

        return True


class EditPageDialog (BasePageDialog):
    def __init__ (self, currentPage, *args, **kwds):
        super (EditPageDialog, self).__init__ (*args, **kwds)
        self.SetTitle(_(u"Edit page properties"))

        assert currentPage is not None
        self._currentPage = currentPage

        map (lambda panel: panel.initBeforeEditing (self._currentPage),
             self._panels)


    def _validate (self):
        for panel in self._panels:
            if not panel.validateBeforeEditing (self._currentPage):
                return False

        return True

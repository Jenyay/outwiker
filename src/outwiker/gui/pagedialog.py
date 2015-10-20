# -*- coding: utf-8 -*-

import wx

import outwiker.core.commands
from .basepagedialog import BasePageDialog
from outwiker.core.tree import RootWikiPage
from outwiker.core.application import Application
from outwiker.core.commands import pageExists, MessageBox
from outwiker.core.style import Style


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
                outwiker.core.commands.MessageBox (_(u"Can't rename page\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

            currentPage.tags = dlg.tags

            try:
                currentPage.icon = dlg.icon
            except EnvironmentError as e:
                outwiker.core.commands.MessageBox (_(u"Can't change page icon\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

            try:
                Style().setPageStyle (currentPage, dlg.style)
            except EnvironmentError as e:
                outwiker.core.commands.MessageBox (_(u"Can't change page style\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

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

                assert page is not None

                page.tags = dlg.tags
                page.icon = dlg.icon
                Style().setPageStyle (page, dlg.style)

                page.root.selectedPage = page
            except EnvironmentError:
                outwiker.core.commands.MessageBox (_(u"Can't create page"), "Error", wx.ICON_ERROR | wx.OK)

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
        self._parentPage = parentPage

        self.SetTitle(_(u"Create Page"))

        map (lambda panel: panel.initBeforeCreation (self._parentPage), self._panels)


    def _validate (self):
        for panel in self._panels:
            if not panel.validateBeforeCreation (self._parentPage):
                return False

        if (self._parentPage is not None and
                not RootWikiPage.testDublicate(self._parentPage, self.pageTitle)):
                    outwiker.core.commands.MessageBox (_(u"A page with some title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)
                    return False
        return True


class EditPageDialog (BasePageDialog):
    def __init__ (self, currentPage, *args, **kwds):
        super (EditPageDialog, self).__init__ (*args, **kwds)
        self.SetTitle(_(u"Edit page properties"))

        assert currentPage is not None
        self._currentPage = currentPage

        map (lambda panel: panel.initBeforeEditing (self._currentPage), self._panels)


    def _validate (self):
        for panel in self._panels:
            if not panel.validateBeforeEditing (self._currentPage):
                return False

        if not self._currentPage.canRename (self.pageTitle):
            outwiker.core.commands.MessageBox (_(u"Can't rename page when page with that title already exists"),
                                               _(u"Error"),
                                               wx.ICON_ERROR | wx.OK)
            return False

        return True

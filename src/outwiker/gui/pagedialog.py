# -*- coding: utf-8 -*-

import wx

import outwiker.core.commands
from .basepagedialog import BasePageDialog
from outwiker.core.tree import RootWikiPage
from outwiker.core.application import Application
from outwiker.core.commands import pageExists, MessageBox
from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList


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

    dlg = EditPageDialog (currentPage, currentPage.parent, parent = parentWnd)

    if dlg.ShowModal() == wx.ID_OK:
        currentPage.tags = dlg.tags
        currentPage.icon = dlg.icon

        try:
            currentPage.title = dlg.pageTitle
        except OSError as e:
            outwiker.core.commands.MessageBox (_(u"Can't rename page\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

        try:
            Style().setPageStyle (currentPage, dlg.style)
        except IOError as e:
            outwiker.core.commands.MessageBox (_(u"Can't change page style\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

        currentPage.root.selectedPage = currentPage

    dlg.Destroy()


@outwiker.core.commands.testreadonly
def createPageWithDialog (parentwnd, parentpage):
    """
    Показать диалог настроек и создать страницу
    """
    if parentpage.readonly:
        raise outwiker.core.exceptions.ReadonlyException

    dlg = CreatePageDialog (parentpage, parentwnd)
    page = None

    if dlg.ShowModal() == wx.ID_OK:
        factory = dlg.selectedFactory
        title = dlg.pageTitle
        tags = dlg.tags

        try:
            page = factory.create (parentpage, title, tags)

            assert page is not None

            page.icon = dlg.icon
            Style().setPageStyle (page, dlg.style)
            page.root.selectedPage = page

        except (OSError, IOError):
            outwiker.core.commands.MessageBox (_(u"Can't create page"), "Error", wx.ICON_ERROR | wx.OK)

    dlg.Destroy()


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
        super (CreatePageDialog, self).__init__ (parentPage, *args, **kwds)
        self.SetTitle(_(u"Create Page"))

        map (lambda panel: panel.initBeforeCreation (parentPage), self._panels)

        self._stylesList = StylesList (getStylesDirList ())
        self._fillStyleCombo (self._stylesList, None)


    def onOk (self, event):
        for panel in self._panels:
            if not panel.validateBeforeCreation (self.parentPage):
                return

        if (self.parentPage is not None and
                not RootWikiPage.testDublicate(self.parentPage, self.pageTitle)):
                    outwiker.core.commands.MessageBox (_(u"A page with this title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)
                    return

        self.saveParams()
        map (lambda panel: panel.saveParams(), self._panels)
        event.Skip()


    @property
    def style (self):
        selItem = self.appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 1]


class EditPageDialog (BasePageDialog):
    def __init__ (self, currentPage, parentPage = None, *args, **kwds):
        super (EditPageDialog, self).__init__ (parentPage, *args, **kwds)
        self.SetTitle(_(u"Edit page properties"))

        assert currentPage is not None
        self.currentPage = currentPage

        map (lambda panel: panel.initBeforeEditing (currentPage), self._panels)

        self._stylesList = StylesList (getStylesDirList ())
        self._fillStyleCombo (self._stylesList, currentPage)


    def onOk (self, event):
        for panel in self._panels:
            if not panel.validateBeforeEditing (self.currentPage):
                return

        if not self.currentPage.canRename (self.pageTitle):
            outwiker.core.commands.MessageBox (_(u"Can't rename page when page with that title already exists"),
                                               _(u"Error"),
                                               wx.ICON_ERROR | wx.OK)
            return

        self.saveParams()
        map (lambda panel: panel.saveParams(), self._panels)
        event.Skip()


    @property
    def style (self):
        selItem = self.appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getPageStyle (self.currentPage)
        elif selItem == 1:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 2]

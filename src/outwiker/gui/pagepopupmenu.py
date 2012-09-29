#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

import outwiker.gui.pagedialog


class PagePopupMenu (object):
    def __init__ (self, parent, popupPage, application):
        self.ID_ADD_CHILD = wx.NewId()
        self.ID_ADD_SIBLING = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_PROPERTIES_POPUP = wx.NewId()

        self.ID_COPY_PATH = wx.NewId()
        self.ID_COPY_ATTACH_PATH = wx.NewId()
        self.ID_COPY_TITLE = wx.NewId()
        self.ID_COPY_LINK = wx.NewId()

        self.parent = parent

        # Страница, над элементом которой вызывается контекстное меню
        self.popupPage = popupPage
        self.menu = self.__createPopupMenu (self.popupPage)

        application.onTreePopupMenu (self.menu, popupPage)


    def __bindPopupMenuEvents (self, popupMenu):
        popupMenu.Bind(wx.EVT_MENU, self.__onAddChild, id=self.ID_ADD_CHILD)
        popupMenu.Bind(wx.EVT_MENU, self.__onAddSibling, id=self.ID_ADD_SIBLING)
        popupMenu.Bind(wx.EVT_MENU, self.__onRemove, id=self.ID_REMOVE)
        popupMenu.Bind(wx.EVT_MENU, self.__onCopyTitle, id=self.ID_COPY_TITLE)
        popupMenu.Bind(wx.EVT_MENU, self.__onCopyPath, id=self.ID_COPY_PATH)
        popupMenu.Bind(wx.EVT_MENU, self.__onCopyAttachPath, id=self.ID_COPY_ATTACH_PATH)
        popupMenu.Bind(wx.EVT_MENU, self.__onCopyLink, id=self.ID_COPY_LINK)
        popupMenu.Bind(wx.EVT_MENU, self.__onPropertiesPopup, id=self.ID_PROPERTIES_POPUP)


    def __onAddChild (self, event):
        assert self.popupPage != None
        outwiker.gui.pagedialog.createPageWithDialog (self.parent, self.popupPage)


    def __onAddSibling (self, event):
        assert self.popupPage != None
        outwiker.gui.pagedialog.createPageWithDialog (self.parent, self.popupPage.parent)


    def __onPropertiesPopup (self, event):
        assert self.popupPage != None
        if self.popupPage.parent != None:
            outwiker.gui.pagedialog.editPage (self.parent, self.popupPage)


    def __createPopupMenu (self, popupPage):
        self.popupPage = popupPage

        popupMenu = wx.Menu ()
        popupMenu.Append (self.ID_ADD_CHILD, _(u"Add Child Page…"))
        popupMenu.Append (self.ID_ADD_SIBLING, _(u"Add Sibling Page…"))
        # popupMenu.Append (self.ID_RENAME, _(u"Rename"))
        popupMenu.Append (self.ID_REMOVE, _(u"Remove…"))
        popupMenu.AppendSeparator()

        popupMenu.Append (self.ID_COPY_TITLE, _(u"Copy Page Title"))
        popupMenu.Append (self.ID_COPY_PATH, _(u"Copy Page Path"))
        popupMenu.Append (self.ID_COPY_ATTACH_PATH, _(u"Copy Attaches Path"))
        popupMenu.Append (self.ID_COPY_LINK, _(u"Copy Page Link"))
        popupMenu.AppendSeparator()

        popupMenu.Append (self.ID_PROPERTIES_POPUP, _(u"Properties…"))

        self.__bindPopupMenuEvents (popupMenu)

        return popupMenu


    def __onRemove (self, event):
        """
        Удалить страницу
        """
        assert self.popupPage != None
        outwiker.core.commands.removePage (self.popupPage)


    def __onCopyLink (self, event):
        """
        Копировать ссылку на страницу в буфер обмена
        """
        assert self.popupPage != None
        outwiker.core.commands.copyLinkToClipboard (self.popupPage)


    def __onCopyTitle (self, event):
        """
        Копировать заголовок страницы в буфер обмена
        """
        assert self.popupPage != None
        outwiker.core.commands.copyTitleToClipboard (self.popupPage)


    def __onCopyPath (self, event):
        """
        Копировать путь до страницы в буфер обмена
        """
        assert self.popupPage != None
        outwiker.core.commands.copyPathToClipboard (self.popupPage)


    def __onCopyAttachPath (self, event):
        """
        Копировать путь до прикрепленных файлов в буфер обмена
        """
        assert self.popupPage != None
        outwiker.core.commands.copyAttachPathToClipboard (self.popupPage)


# -*- coding: UTF-8 -*-

import wx


class MainMenu(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

        self.fileMenu = wx.Menu()
        self.Append(self.fileMenu, _(u"File"))

        self.editMenu = self._createEditMenu()
        self.Append(self.editMenu, _(u"Edit"))

        self.treeMenu = wx.Menu()
        self.Append(self.treeMenu, _(u"Tree"))

        self.toolsMenu = wx.Menu()
        self.Append(self.toolsMenu, _(u"Tools"))

        self.bookmarksMenu = wx.Menu()
        self.Append(self.bookmarksMenu, _(u"Bookmarks"))

        self.viewMenu = self._createViewMenu()
        self.Append(self.viewMenu, _(u"View"))

        self.helpMenu = wx.Menu()
        self.Append(self.helpMenu, _(u"Help"))

    def _createViewMenu(self):
        viewMenu = wx.Menu()
        self.switchToMenu = wx.Menu()
        viewMenu.AppendSubMenu(self.switchToMenu, _(u'Go to'))
        return viewMenu

    def _createEditMenu(self):
        editMenu = wx.Menu()

        editMenu.Append(wx.ID_UNDO,
                        _(u"Undo") + "\tCtrl+Z",
                        "",
                        wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_REDO,
                        _(u"Redo") + "\tCtrl+Y",
                        "",
                        wx.ITEM_NORMAL)

        editMenu.AppendSeparator()

        editMenu.Append(wx.ID_CUT,
                        _(u"Cut") + "\tCtrl+X",
                        "",
                        wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_COPY,
                        _(u"Copy") + "\tCtrl+C",
                        "",
                        wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_PASTE,
                        _(u"Paste") + "\tCtrl+V",
                        "",
                        wx.ITEM_NORMAL)

        editMenu.AppendSeparator()

        editMenu.Append(wx.ID_SELECTALL,
                        _(u"Select All") + "\tCtrl+A",
                        "",
                        wx.ITEM_NORMAL)

        return editMenu

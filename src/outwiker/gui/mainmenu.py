# -*- coding: UTF-8 -*-

import wx

from .mainid import MainId


class MainMenu (wx.MenuBar):
    """
    Класс главного окна
    """
    def __init__ (self):
        wx.MenuBar.__init__ (self)

        self.fileMenu = wx.Menu()
        self.Append(self.fileMenu, _("File"))

        self.editMenu = self.__createEditMenu()
        self.Append(self.editMenu, _("Edit"))

        self.treeMenu = wx.Menu()
        self.Append(self.treeMenu, _("Tree"))

        self.toolsMenu = wx.Menu()
        self.Append(self.toolsMenu, _("Tools"))

        self.bookmarksMenu = wx.Menu ()
        self.Append(self.bookmarksMenu, _("Bookmarks"))

        self.viewMenu = wx.Menu()
        self.Append(self.viewMenu, _("View"))

        self.helpMenu = wx.Menu()
        self.Append(self.helpMenu, _("Help"))


    def __createEditMenu (self):
        editMenu = wx.Menu()

        editMenu.Append (MainId.ID_UNDO,
                         _("Undo") + "\tCtrl+Z",
                         "",
                         wx.ITEM_NORMAL)

        editMenu.Append (MainId.ID_REDO,
                         _("Redo") + "\tCtrl+Y",
                         "",
                         wx.ITEM_NORMAL)

        editMenu.AppendSeparator()

        editMenu.Append (MainId.ID_CUT,
                         _("Cut") + "\tCtrl+X",
                         "",
                         wx.ITEM_NORMAL)

        editMenu.Append (MainId.ID_COPY,
                         _("Copy") + "\tCtrl+C",
                         "",
                         wx.ITEM_NORMAL)

        editMenu.Append (MainId.ID_PASTE,
                         _("Paste") + "\tCtrl+V",
                         "",
                         wx.ITEM_NORMAL)

        return editMenu

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from .mainid import MainId
from outwiker.core.system import getImagesDir


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

        self.toolsMenu = self.__createToolsMenu ()
        self.Append(self.toolsMenu, _("Tools"))

        self.bookmarksMenu = wx.Menu ()
        self.Append(self.bookmarksMenu, _("Bookmarks"))

        self.viewMenu = wx.Menu()
        self.Append(self.viewMenu, _("View"))

        self.helpMenu = self.__createHelpMenu ()
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


    def __createToolsMenu (self):
        toolsMenu = wx.Menu()

        toolsMenu.Append(MainId.ID_ATTACH, 
                _(u"Attach Files…") + "\tCtrl+Alt+A", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.AppendSeparator()

        toolsMenu.Append(MainId.ID_COPY_TITLE, 
                _(u"Copy Page Title") + "\tCtrl+Shift+D", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_COPYPATH, 
                _(u"Copy Page Path") + "\tCtrl+Shift+P", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_COPY_ATTACH_PATH, 
                _(u"Copy Attachments Path") + "\tCtrl+Shift+A", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_COPY_LINK, 
                _(u"Copy Page Link") + "\tCtrl+Shift+L", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.AppendSeparator()

        toolsMenu.Append (MainId.ID_ADD_TAGS_TO_BRANCH, 
                _(u"Add Tags to Branch…"), 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append (MainId.ID_REMOVE_TAGS_FROM_BRANCH, 
                _(u"Remove Tags from Branch…"), 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append (MainId.ID_RENAME_TAG, 
                _(u"Rename Tag…"), 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.AppendSeparator()

        toolsMenu.Append(MainId.ID_RELOAD, 
                _(u"Reload Wiki…") + "\tCtrl+R", 
                "", 
                wx.ITEM_NORMAL)

        return toolsMenu


    def __createHelpMenu (self):
        helpMenu = wx.Menu()
        helpMenu.Append(MainId.ID_HELP, 
                _("Help") + "\tF1", 
                "", 
                wx.ITEM_NORMAL)

        helpMenu.Append(MainId.ID_ABOUT, 
                _(u"About…") + "\tCtrl+F1", 
                "", 
                wx.ITEM_NORMAL)

        return helpMenu


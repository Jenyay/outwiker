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

        self.fileMenu = self.__createFileMenu ()
        self.Append(self.fileMenu, _("File"))

        self.editMenu = self.__createEditMenu()
        self.Append(self.editMenu, _("Edit"))

        self.treeMenu = self.__createTreeMenu()
        self.Append(self.treeMenu, _("Tree"))

        self.toolsMenu = self.__createToolsMenu ()
        self.Append(self.toolsMenu, _("Tools"))

        self.bookmarksMenu = self.__createBookmarksMenu ()
        self.Append(self.bookmarksMenu, _("Bookmarks"))

        self.viewMenu = self.__createViewMenu ()
        self.Append(self.viewMenu, _("View"))

        self.helpMenu = self.__createHelpMenu ()
        self.Append(self.helpMenu, _("Help"))


    def __createFileMenu (self):
        fileMenu = wx.Menu()

        fileMenu.Append (MainId.ID_SAVE, 
                _("Save") + "\tCtrl+S", 
                "", 
                wx.ITEM_NORMAL)

        fileMenu.AppendSeparator()

        fileMenu.Append (wx.ID_PRINT, 
                _("Print") + "\tCtrl+P", 
                "", 
                wx.ITEM_NORMAL)

        fileMenu.Append (MainId.ID_EXIT, 
                _(u"Exit…") + "\tAlt+F4", 
                "", 
                wx.ITEM_NORMAL)

        fileMenu.AppendSeparator()
    
        return fileMenu


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

        editMenu.AppendSeparator()

        editMenu.Append (MainId.ID_PREFERENCES, 
                _(u"Preferences…") + "\tCtrl+F8", 
                "", 
                wx.ITEM_NORMAL)

        return editMenu


    def __createTreeMenu (self):
        treeMenu = wx.Menu()

        treeMenu.Append(MainId.ID_ADDPAGE, 
                _(u"Add Sibling Page…") + "\tCtrl+Alt+T", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.Append(MainId.ID_ADDCHILD, 
                _(u"Add Child Page…") + "\tCtrl+Shift+T", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.AppendSeparator()

        treeMenu.Append(MainId.ID_MOVE_PAGE_UP, 
                _("Move Page Up") + "\tCtrl+Shift+Up", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.Append(MainId.ID_MOVE_PAGE_DOWN, 
                _("Move Page Down") + "\tCtrl+Shift+Down", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.Append(MainId.ID_SORT_CHILDREN_ALPHABETICAL, 
                _("Sort Children Pages Alphabetical"), 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.Append(MainId.ID_SORT_SIBLINGS_ALPHABETICAL, 
                _("Sort Siblings Pages Alphabetical"), 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.AppendSeparator()

        treeMenu.Append(MainId.ID_RENAME, 
                _("Rename Page") + "\tF2", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.Append(MainId.ID_REMOVE_PAGE, 
                _(u"Remove Page…") + "\tCtrl+Shift+Del", 
                "", 
                wx.ITEM_NORMAL)

        treeMenu.AppendSeparator()

        treeMenu.Append(MainId.ID_EDIT, 
                _(u"Page Properties…") + "\tCtrl+E", 
                "", 
                wx.ITEM_NORMAL)

        return treeMenu


    def __createToolsMenu (self):
        toolsMenu = wx.Menu()

        toolsMenu.Append(MainId.ID_ADD_TAB, 
                _(u"Add Tab") + "\tCtrl+T", 
                "",
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_CLOSE_TAB, 
                _(u"Close Tab") + "\tCtrl+W", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_PREV_TAB, 
                _(u"Previous Tab") + "\tCtrl+Shift+PgUp", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.Append(MainId.ID_NEXT_TAB, 
                _(u"Next Tab") + "\tCtrl+Shift+PgDn", 
                "", 
                wx.ITEM_NORMAL)

        toolsMenu.AppendSeparator()

        toolsMenu.Append(MainId.ID_GLOBAL_SEARCH, 
                _(u"Global Search…") + "\tCtrl+Shift+F", 
                "", 
                wx.ITEM_NORMAL)

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


    def __createBookmarksMenu (self):
        bookmarksMenu = wx.Menu()

        bookmarksMenu.Append(MainId.ID_ADDBOOKMARK, 
                _("Add/Remove Bookmark") + "\tCtrl+D", 
                "", 
                wx.ITEM_NORMAL)

        bookmarksMenu.AppendSeparator()

        return bookmarksMenu


    def __createViewMenu (self):
        viewMenu = wx.Menu()

        self.viewNotes = wx.MenuItem(
                viewMenu, 
                MainId.ID_VIEW_TREE, 
                _("Notes Tree"), 
                "", 
                wx.ITEM_CHECK)
        viewMenu.AppendItem(self.viewNotes)

        self.viewAttaches = wx.MenuItem(
                viewMenu, 
                MainId.ID_VIEW_ATTACHES, 
                _("Attachments"), 
                "", 
                wx.ITEM_CHECK)
        viewMenu.AppendItem(self.viewAttaches)


        self.viewTagsCloud = wx.MenuItem(
                viewMenu, 
                MainId.ID_VIEW_TAGSCLOUD, 
                _("Tags"), 
                "", 
                wx.ITEM_CHECK)
        viewMenu.AppendItem(self.viewTagsCloud)

        viewMenu.AppendSeparator()

        self.viewFullscreen = wx.MenuItem(
                viewMenu, 
                MainId.ID_VIEW_FULLSCREEN, 
                _("Fullscreen") + "\tF11", 
                "", 
                wx.ITEM_CHECK)
        viewMenu.AppendItem(self.viewFullscreen)

        return viewMenu


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


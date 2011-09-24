#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from .mainid import MainId
from core.system import getImagesDir


class MainMenu (wx.MenuBar):
	"""
	Класс главного окна
	"""

	def __init__ (self):
		wx.MenuBar.__init__ (self)

		self.fileMenu = self.__createFileMenu ()
		self.Append(self.fileMenu, _("&File"))

		self.editMenu = self.__createEditMenu()
		self.Append(self.editMenu, _("&Edit"))

		self.treeMenu = self.__createTreeMenu()
		self.Append(self.treeMenu, _("&Tree"))

		self.toolsMenu = self.__createToolsMenu ()
		self.Append(self.toolsMenu, _("T&ools"))

		self.bookmarksMenu = self.__createBookmarksMenu ()
		self.Append(self.bookmarksMenu, _("&Bookmarks"))

		self.viewMenu = self.__createViewMenu ()
		self.Append(self.viewMenu, _("&View"))

		self.helpMenu = self.__createHelpMenu ()
		self.Append(self.helpMenu, _("&Help"))


	def __createFileMenu (self):
		fileMenu = wx.Menu()
		fileMenu.Append(MainId.ID_NEW, _(u"&New…\tCtrl+N"), "", wx.ITEM_NORMAL)
		fileMenu.Append(MainId.ID_OPEN, _(u"&Open…\tCtrl+O"), "", wx.ITEM_NORMAL)
		fileMenu.Append(MainId.ID_OPEN_READONLY, _(u"Open &Read-only…\tCtrl+Shift+O"), "", wx.ITEM_NORMAL)
		fileMenu.Append(MainId.ID_SAVE, _("&Save\tCtrl+S"), "", wx.ITEM_NORMAL)
		fileMenu.Append(wx.ID_PRINT, _("&Print\tCtrl+P"), "", wx.ITEM_NORMAL)
		fileMenu.Append(MainId.ID_EXIT, _(u"&Exit…\tAlt+F4"), "", wx.ITEM_NORMAL)
		fileMenu.AppendSeparator()
	
		return fileMenu


	def __createEditMenu (self):
		editMenu = wx.Menu()
		editMenu.Append(MainId.ID_UNDO, _("&Undo\tCtrl+Z"), "", wx.ITEM_NORMAL)
		editMenu.Append(MainId.ID_REDO, _("&Redo\tCtrl+Y"), "", wx.ITEM_NORMAL)
		editMenu.AppendSeparator()
		editMenu.Append(MainId.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
		editMenu.Append(MainId.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
		editMenu.Append(MainId.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
		editMenu.AppendSeparator()
		editMenu.Append(MainId.ID_PREFERENCES, _(u"Pr&eferences…\tCtrl+F8"), "", wx.ITEM_NORMAL)

		return editMenu


	def __createTreeMenu (self):
		treeMenu = wx.Menu()
		treeMenu.Append(MainId.ID_ADDPAGE, _(u"Add &Sibling Page…\tCtrl+T"), "", wx.ITEM_NORMAL)
		treeMenu.Append(MainId.ID_ADDCHILD, _(u"Add &Child Page…\tCtrl+Shift+T"), "", wx.ITEM_NORMAL)
		treeMenu.AppendSeparator()
		treeMenu.Append(MainId.ID_MOVE_PAGE_UP, _("Move Page Up\tCtrl+Shift+Up"), "", wx.ITEM_NORMAL)
		treeMenu.Append(MainId.ID_MOVE_PAGE_DOWN, _("Move Page Down\tCtrl+Shift+Down"), "", wx.ITEM_NORMAL)
		treeMenu.Append(MainId.ID_SORT_CHILDREN_ALPHABETICAL, _("Sort Children Pages Alphabetical"), "", wx.ITEM_NORMAL)
		treeMenu.Append(MainId.ID_SORT_SIBLINGS_ALPHABETICAL, _("Sort Siblings Pages Alphabetical"), "", wx.ITEM_NORMAL)
		treeMenu.AppendSeparator()
		treeMenu.Append(MainId.ID_RENAME, _("Re&name Page\tF2"), "", wx.ITEM_NORMAL)
		treeMenu.Append(MainId.ID_REMOVE_PAGE, _(u"Rem&ove Page…\tCtrl+Shift+Del"), "", wx.ITEM_NORMAL)
		treeMenu.AppendSeparator()
		treeMenu.Append(MainId.ID_EDIT, _(u"Pag&e Properties…\tCtrl+E"), "", wx.ITEM_NORMAL)

		return treeMenu


	def __createToolsMenu (self):
		toolsMenu = wx.Menu()
		toolsMenu.Append(MainId.ID_GLOBAL_SEARCH, _(u"&Global Search…\tCtrl+Shift+F"), "", wx.ITEM_NORMAL)
		toolsMenu.Append(MainId.ID_ATTACH, _(u"&Attach Files…\tCtrl+Alt+A"), "", wx.ITEM_NORMAL)
		toolsMenu.AppendSeparator()
		toolsMenu.Append(MainId.ID_COPY_TITLE, _("Copy Page &Title\tCtrl+Shift+D"), "", wx.ITEM_NORMAL)
		toolsMenu.Append(MainId.ID_COPYPATH, _("Copy &Page Path\tCtrl+Shift+P"), "", wx.ITEM_NORMAL)
		toolsMenu.Append(MainId.ID_COPY_ATTACH_PATH, _("Copy Atta&ches Path\tCtrl+Shift+A"), "", wx.ITEM_NORMAL)
		toolsMenu.Append(MainId.ID_COPY_LINK, _("Copy Page &Link\tCtrl+Shift+L"), "", wx.ITEM_NORMAL)
		toolsMenu.AppendSeparator()
		toolsMenu.Append(MainId.ID_RELOAD, _(u"&Reload Wiki…\tCtrl+R"), "", wx.ITEM_NORMAL)

		return toolsMenu


	def __createBookmarksMenu (self):
		bookmarksMenu = wx.Menu()
		bookmarksMenu.Append(MainId.ID_ADDBOOKMARK, _("&Add/Remove Bookmark\tCtrl+D"), "", wx.ITEM_NORMAL)
		bookmarksMenu.AppendSeparator()

		return bookmarksMenu


	def __createViewMenu (self):
		viewMenu = wx.Menu()
		self.viewNotes = wx.MenuItem(viewMenu, MainId.ID_VIEW_TREE, _("Notes &Tree"), "", wx.ITEM_CHECK)
		viewMenu.AppendItem(self.viewNotes)

		self.viewAttaches = wx.MenuItem(viewMenu, MainId.ID_VIEW_ATTACHES, _("Attaches"), "", wx.ITEM_CHECK)
		viewMenu.AppendItem(self.viewAttaches)

		viewMenu.AppendSeparator()
		self.viewFullscreen = wx.MenuItem(viewMenu, MainId.ID_VIEW_FULLSCREEN, _("Fullscreen\tF11"), "", wx.ITEM_CHECK)
		viewMenu.AppendItem(self.viewFullscreen)

		return viewMenu


	def __createHelpMenu (self):
		helpMenu = wx.Menu()
		helpMenu.Append(MainId.ID_HELP, _("&Help\tF1"), "", wx.ITEM_NORMAL)
		helpMenu.Append(MainId.ID_ABOUT, _(u"&About…\tCtrl+F1"), "", wx.ITEM_NORMAL)

		return helpMenu


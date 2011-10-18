#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.application import Application
from .bookmarkscontroller import BookmarksController
from .mainid import MainId
import outwiker.core.commands


class MainWndController (object):
	"""
	Контроллер для управления главным окном
	"""

	def __init__ (self, parent):
		"""
		parent - окно, которым управляет контроллер
		"""
		self.parent = parent

		# Идентификаторы пунктов меню и кнопок, которые надо задизаблить, если не открыта вики
		self.disabledTools = [MainId.ID_SAVE, MainId.ID_RELOAD, 
				MainId.ID_ADDPAGE, MainId.ID_ADDCHILD, MainId.ID_ATTACH, 
				MainId.ID_COPYPATH, MainId.ID_COPY_ATTACH_PATH, MainId.ID_COPY_LINK,
				MainId.ID_COPY_TITLE, MainId.ID_BOOKMARKS, MainId.ID_ADDBOOKMARK,
				MainId.ID_EDIT, MainId.ID_REMOVE_PAGE, MainId.ID_GLOBAL_SEARCH,
				MainId.ID_UNDO, MainId.ID_REDO, MainId.ID_CUT, MainId.ID_COPY, MainId.ID_PASTE,
				MainId.ID_SORT_SIBLINGS_ALPHABETICAL, MainId.ID_SORT_CHILDREN_ALPHABETICAL,
				MainId.ID_MOVE_PAGE_UP, MainId.ID_MOVE_PAGE_DOWN, MainId.ID_RENAME]

		# Идентификаторы для пунктов меню последних открытых вики
		# Ключ - id, значение - путь до вики
		self._recentId = {}

		self.bookmarks = BookmarksController (self)


		self.init()


	def init (self):
		"""
		Начальные установки для главного окна
		"""
		self.__bindAppEvents()


	def destroy (self):
		self.__unbindAppEvents()


	@property
	def mainWindow (self):
		return self.parent


	@property
	def mainMenu (self):
		return self.mainWindow.mainMenu


	def removeMenuItemsById (self, menu, keys):
		"""
		Удалить все элементы меню по идентификаторам
		"""
		for key in keys:
			menu.Delete (key)
			self.mainWindow.Unbind (wx.EVT_MENU, id = key)



	def __bindAppEvents (self):
		Application.onPageSelect += self.__onPageSelect
		Application.onPreferencesDialogClose += self.__onPreferencesDialogClose
		Application.onBookmarksChanged += self.__onBookmarksChanged
		Application.onTreeUpdate += self.__onTreeUpdate
		Application.onWikiOpen += self.__onWikiOpen


	def __unbindAppEvents (self):
		Application.onPageSelect -= self.__onPageSelect
		Application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
		Application.onBookmarksChanged -= self.__onBookmarksChanged
		Application.onTreeUpdate -= self.__onTreeUpdate
		Application.onWikiOpen -= self.__onWikiOpen


	def __onBookmarksChanged (self, event):
		self.bookmarks.updateBookmarks()


	def __onTreeUpdate (self, sender):
		"""
		Событие при обновлении дерева
		"""
		self.updateBookmarks()
		self.updateTitle()


	def __onWikiOpen (self, wikiroot):
		"""
		Обновить окно после того как загрузили вики
		"""
		if wikiroot != None and not wikiroot.readonly:
			try:
				Application.recentWiki.add (wikiroot.path)
				self.updateRecentMenu()
			except IOError as e:
				outwiker.core.commands.MessageBox (
						_(u"Can't add wiki to recent list.\nCan't save config.\n%s") % (unicode (e)),
						_(u"Error"), wx.ICON_ERROR | wx.OK)

		self.enableGui()
		self.updateBookmarks()
		self.updateTitle()


	def updateBookmarks (self):
		self.bookmarks.updateBookmarks()
	

	###################################################
	# Обработка событий
	#
	def __onPageSelect (self, newpage):
		"""
		Обработчик события выбора страницы в дереве
		"""
		self.updateTitle()


	def __onPreferencesDialogClose (self, prefDialog):
		"""
		Обработчик события изменения настроек главного окна
		"""
		self.updateTitle()
	#
	###################################################


	###################################################
	# Активировать/дизактивировать интерфейс
	#
	def enableGui (self):
		"""
		Проверить открыта ли вики и включить или выключить кнопки на панели
		"""
		enabled = Application.wikiroot != None

		self.__enableTools (enabled)
		self.__enableMenu (enabled)
		self.mainWindow.pagePanel.Enable(enabled)
		self.mainWindow.tree.Enable(enabled)
		self.mainWindow.attachPanel.Enable(enabled)


	def __enableTools (self, enabled):
		for toolId in self.disabledTools:
			if self.mainWindow.mainToolbar.FindById (toolId) != None:
				self.mainWindow.mainToolbar.EnableTool (toolId, enabled)

	
	def __enableMenu (self, enabled):
		for toolId in self.disabledTools:
			if self.mainMenu.FindItemById (toolId) != None:
				self.mainMenu.Enable (toolId, enabled)
	#
	###################################################


	def updateTitle (self):
		"""
		Обновить заголовок главного окна в зависимости от шаблона и текущей страницы
		"""
		template = self.mainWindow.mainWindowConfig.titleFormatOption.value

		if Application.wikiroot == None:
			self.mainWindow.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if Application.wikiroot.selectedPage == None else Application.wikiroot.selectedPage.title
		filename = os.path.basename (Application.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.mainWindow.SetTitle (result)


	def loadMainWindowParams(self):
		"""
		Загрузить параметры из конфига
		"""
		self.mainWindow.Freeze()

		width = self.mainWindow.mainWindowConfig.WidthOption.value
		height = self.mainWindow.mainWindowConfig.HeightOption.value

		xpos = self.mainWindow.mainWindowConfig.XPosOption.value
		ypos = self.mainWindow.mainWindowConfig.YPosOption.value
		
		self.mainWindow.SetDimensions (xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

		self.mainWindow.Layout()
		self.mainWindow.Thaw()


	###################################################
	# Список последних открытых вики
	#
	def updateRecentMenu (self):
		"""
		Обновление меню со списком последних открытых вики
		"""
		self.removeMenuItemsById (self.mainMenu.fileMenu, self._recentId.keys())
		self._recentId = {}

		for n in range (len (Application.recentWiki)):
			id = wx.NewId()
			path = Application.recentWiki[n]
			self._recentId[id] = path

			title = path if n + 1 > 9 else u"&{n}. {path}".format (n=n+1, path=path)

			self.mainMenu.fileMenu.Append (id, title, "", wx.ITEM_NORMAL)
			
			self.mainWindow.Bind(wx.EVT_MENU, self.__onRecent, id=id)
	

	def __onRecent (self, event):
		"""
		Выбор пункта меню с недавно открытыми файлами
		"""
		outwiker.core.commands.openWiki (self._recentId[event.Id])

	#
	###################################################

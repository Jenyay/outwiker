#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

from core.tree import RootWikiPage
from core.controller import Controller
import core.system

class BaseTextPanel (wx.Panel):
	"""
	Базовый класс для представления текстовых страниц и им подобных (где есть текстовый редактор)
	"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def GetContentFromGui(self):
		"""
		Получить из интерфейса контент, который будет сохранен в файл __page.text
		"""
		pass


	@abstractmethod
	def GetSearchPanel (self):
		"""
		Вернуть панель поиска
		"""
		pass

	
	def __init__ (self, *args, **kwds):
		self._currentpage = None
		self.mainWindow = None
		self.searchMenu = None

		self.ID_SEARCH = wx.NewId()
		self.ID_SEARCH_NEXT = wx.NewId()
		self.ID_SEARCH_PREV = wx.NewId()

		self.searchMenuIndex = 2
		self.imagesDir = core.system.getImagesDir()

		Controller.instance().onAttachmentPaste += self.onAttachmentPaste
		Controller.instance().onEditorConfigChange += self.onEditorConfigChange

	
	def onEditorConfigChange (self):
		pass
	

	@property
	def page (self):
		return self._currentpage


	@page.setter
	def page (self, page):
		self._currentpage = page
		self.UpdateView (page)
	

	def Save (self):
		"""
		Сохранить страницу
		"""
		if self.page != None and not self.page.isRemoved and not self.page.readonly:
			self.page.content = self.GetContentFromGui()
	

	def UpdateView (self, page):
		"""
		Обновление страницы
		"""
		pass


	def onAttachmentPaste (self, fnames):
		"""
		Пользователь хочет вставить ссылки на приаттаченные файлы
		"""
		pass



	def Close (self):
		"""
		Закрытие панели. 
		Вызывать вручную!!!
		"""
		Controller.instance().onAttachmentPaste -= self.onAttachmentPaste
		Controller.instance().onEditorConfigChange -= self.onEditorConfigChange

		self.Save()
		self.Destroy()
	

	def _getAttachString (self, fnames):
		text = ""
		count = len (fnames)

		for n in range (count):
			text += RootWikiPage.attachDir + "/" + fnames[n]
			if n != count -1:
				text += "\n"

		return text

	
	def initGui (self, mainWindow):
		"""
		Добавить элементы управления в главное окно
		"""
		self.mainWindow = mainWindow

		self._addMenuItems ()
		self._addToolsItems ()


	def removeGui (self):
		"""
		Убрать за собой элементы управления
		"""
		assert self.mainWindow != None

		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH)
		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_NEXT)
		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_PREV)

		self.mainWindow.mainMenu.Remove (self.searchMenuIndex)
		
		self.mainWindow.mainToolbar.DeleteTool (self.ID_SEARCH)

	
	def _addMenuItems (self):
		"""
		Добавить пункты меню
		"""
		assert self.mainWindow != None

		self.searchMenu = wx.Menu()

		self.searchMenu.Append (self.ID_SEARCH, _(u"Search…\tCtrl+F"), "", wx.ITEM_NORMAL)
		self.searchMenu.Append (self.ID_SEARCH_NEXT, _(u"Find next\tF3"), "", wx.ITEM_NORMAL)
		self.searchMenu.Append (self.ID_SEARCH_PREV, _(u"Find previous\tShift+F3"), "", wx.ITEM_NORMAL)
		
		self.mainWindow.mainMenu.Insert (self.searchMenuIndex, self.searchMenu, _("&Search") )

		self.mainWindow.Bind(wx.EVT_MENU, self.onSearch, id=self.ID_SEARCH)
		self.mainWindow.Bind(wx.EVT_MENU, self.onSearchNext, id=self.ID_SEARCH_NEXT)
		self.mainWindow.Bind(wx.EVT_MENU, self.onSearchPrev, id=self.ID_SEARCH_PREV)
	

	def _addToolsItems (self):
		self.mainWindow.mainToolbar.AddLabelTool(self.ID_SEARCH, 
				_(u"Search"),
				wx.Bitmap(os.path.join (self.imagesDir, "local_search.png"), wx.BITMAP_TYPE_ANY), 
				wx.NullBitmap, 
				wx.ITEM_NORMAL, 
				_(u"Search"),
				"")

		self.mainWindow.mainToolbar.Realize()
	

	def onSearch (self, event):
		self.GetSearchPanel().startSearch()


	def onSearchNext (self, event):
		self.GetSearchPanel().nextSearch()


	def onSearchPrev (self, event):
		self.GetSearchPanel().prevSearch()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from .basepagepanel import BasePagePanel


class BaseTextPanel (BasePagePanel):
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

	
	def __init__ (self, parent, *args, **kwds):
		BasePagePanel.__init__ (self, parent, *args, **kwds)

		self.mainWindow = Application.mainWindow
		self.searchMenu = None

		self.ID_SEARCH = wx.NewId()
		self.ID_SEARCH_NEXT = wx.NewId()
		self.ID_SEARCH_PREV = wx.NewId()

		self.searchMenuIndex = 2
		self.imagesDir = outwiker.core.system.getImagesDir()

		self._addMenuItems ()
		self._addToolsItems ()

		Application.onAttachmentPaste += self.onAttachmentPaste
		Application.onEditorConfigChange += self.onEditorConfigChange
		Application.onForceSave += self.onForceSave


	def onForceSave (self):
		self.Save()

	
	def onEditorConfigChange (self):
		pass
	

	def Save (self):
		"""
		Сохранить страницу
		"""
		if self.page == None:
			return

		if not os.path.exists (self.page.path) and not self.page.isRemoved:
			# Похоже, страница удалена вручную
			outwiker.core.commands.MessageBox (_(u"Page %s not found. It is recommended to update the wiki") % self.page.title,
					_("Error"), wx.OR | wx.ICON_ERROR )
			return

		if self.page != None and not self.page.isRemoved and not self.page.readonly:
			try:
				self.page.content = self.GetContentFromGui()
			except IOError as e:
				# TODO: Проверить под Windows
				outwiker.core.commands.MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
					_(u"Error"), 
					wx.ICON_ERROR | wx.OK)
	

	def _getAttachString (self, fnames):
		"""
		Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений
		"""
		text = ""
		count = len (fnames)

		for n in range (count):
			text += Attachment.attachDir + "/" + fnames[n]
			if n != count -1:
				text += "\n"

		return text

	
	def Clear (self):
		"""
		Убрать за собой
		"""
		Application.onAttachmentPaste -= self.onAttachmentPaste
		Application.onEditorConfigChange -= self.onEditorConfigChange
		Application.onForceSave -= self.onForceSave

		self.removeGui()


	def removeGui (self):
		"""
		Убрать за собой элементы управления
		"""
		assert self.mainWindow != None
		assert self.mainWindow.mainMenu.GetMenuCount() >= 3
		assert self.searchMenu != None

		#import traceback
		#traceback.print_stack()
		#print 

		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH)
		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_NEXT)
		self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_PREV)

		self.mainWindow.mainMenu.Remove (self.searchMenuIndex)
		self.searchMenu = None

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
	

	def _showSearchPanel (self, panel):
		if not panel.IsShown():
			panel.Show()
			panel.GetParent().Layout()


	def onSearch (self, event):
		panel = self.GetSearchPanel()
		if panel != None:
			self._showSearchPanel (panel)
			panel.startSearch()


	def onSearchNext (self, event):
		panel = self.GetSearchPanel()
		if panel != None:
			self._showSearchPanel (panel)
			panel.nextSearch()


	def onSearchPrev (self, event):
		panel = self.GetSearchPanel()
		if panel != None:
			self._showSearchPanel (panel)
			panel.prevSearch()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

import core.system
import core.commands
from core.attachment import Attachment
from core.application import Application


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

		Application.onAttachmentPaste += self.onAttachmentPaste
		Application.onEditorConfigChange += self.onEditorConfigChange
		Application.onForceSave += self.onForceSave


	def onForceSave (self):
		self.Save()

	
	def onEditorConfigChange (self):
		pass
	

	@property
	def page (self):
		return self._currentpage


	@page.setter
	def page (self, page):
		self._currentpage = page

		if not os.path.exists (page.path):
			core.commands.MessageBox (
					_(u"Page %s not found. It is recommended to update the wiki") % self.page.title,
					_("Error"), wx.OR | wx.ICON_ERROR )
			#core.commands.openWiki (Application.wikiroot.path)
			return

		self.UpdateView (page)
	

	def Save (self):
		"""
		Сохранить страницу
		"""
		if not os.path.exists (self.page.path):
			# Похоже, страница удалена вручную
			core.commands.MessageBox (_(u"Page %s not found. It is recommended to update the wiki") % self.page.title,
					_("Error"), wx.OR | wx.ICON_ERROR )
			#core.commands.openWiki (Application.wikiroot.path)
			return

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
		self.Save()
		self.CloseWithoutSave()
	

	def CloseWithoutSave (self):
		"""
		Закрытие панели без сохранения. 
		"""
		self.Clear()
		wx.Panel.Close (self)
		self.Destroy()
	

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

	
	def initGui (self, mainWindow):
		"""
		Добавить элементы управления в главное окно
		"""
		self.mainWindow = mainWindow

		self._addMenuItems ()
		self._addToolsItems ()


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

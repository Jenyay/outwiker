#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from core.application import Application
from .mainid import MainId


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

		self.init()


	def init (self):
		"""
		Начальные установки для главного окна
		"""
		Application.onPageSelect += self.__onPageSelect
		Application.onMainWindowConfigChange += self.__onMainWindowConfigChange

		self.enableGui()
	

	###################################################
	# Обработка событий
	#
	def __onPageSelect (self, newpage):
		"""
		Обработчик события выбора страницы в дереве
		"""
		self.updateTitle()


	def __onMainWindowConfigChange (self):
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
		self.parent.pagePanel.Enable(enabled)
		self.parent.tree.Enable(enabled)
		self.parent.attachPanel.Enable(enabled)


	def __enableTools (self, enabled):
		for toolId in self.disabledTools:
			if self.parent.mainToolbar.FindById (toolId) != None:
				self.parent.mainToolbar.EnableTool (toolId, enabled)

	
	def __enableMenu (self, enabled):
		for toolId in self.disabledTools:
			if self.parent.mainMenu.FindItemById (toolId) != None:
				self.parent.mainMenu.Enable (toolId, enabled)
	#
	###################################################


	def updateTitle (self):
		"""
		Обновить заголовок главного окна в зависимости от шаблона и текущей страницы
		"""
		template = self.parent.mainWindowConfig.titleFormatOption.value

		if Application.wikiroot == None:
			self.parent.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if Application.wikiroot.selectedPage == None else Application.wikiroot.selectedPage.title
		filename = os.path.basename (Application.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.parent.SetTitle (result)

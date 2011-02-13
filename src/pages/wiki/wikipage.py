#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from core.tree import WikiPage
from wikipanel import WikiPagePanel
import WikiPreferences
from core.config import BooleanOption, IntegerOption
from core.application import Application
from core.factory import PageFactory


class WikiWikiPage (WikiPage):
	"""
	Класс wiki-страниц
	"""
	def __init__ (self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	

	@staticmethod
	def getTypeString ():
		return u"wiki"


class WikiPageFactory (PageFactory):
	@staticmethod
	def getPageType():
		return WikiWikiPage

	# Обрабатываемый этой фабрикой тип страниц (имеется в виду тип, описываемый строкой)
	@staticmethod
	def getTypeString ():
		return WikiPageFactory.getPageType().getTypeString()

	# Название страницы, показываемое пользователю
	title = _(u"Wiki Page")

	# Настройки
	# Показывать вкладку с HTML-кодом?
	showHtmlCodeOptions = BooleanOption (Application.config, "Wiki", "ShowHtmlCode", True)

	# Размер превьюшек по умолчанию
	thumbSizeOptions = IntegerOption (Application.config, "Wiki", "ThumbSize", 250)
	
	# Показывать список прикрепленных файлов вместо пустой страницы?
	showAttachInsteadBlankOptions = BooleanOption (Application.config, "Wiki", "ShowAttachInsteadBlank", True)


	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return PageFactory.createPage (WikiPageFactory.getPageType(), parent, title, tags)


	#@staticmethod
	#def load (path, parent, readonly):


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = WikiPagePanel (parent)
		panel.page = page

		return panel


	@staticmethod
	def getPrefPanels (parent):
		"""
		Получить список панелей для окна настроек
		Возвращает список кортежей ("название", Панель)
		"""
		generalPanel = WikiPreferences.WikiPrefGeneralPanel (parent)

		return [ ( _("General"), generalPanel ) ]


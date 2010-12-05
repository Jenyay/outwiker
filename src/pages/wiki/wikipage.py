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


class WikiWikiPage (WikiPage):
	"""
	Класс wiki-страниц
	"""
	def __init__ (self, path, subpath, create = False):
		WikiPage.__init__ (self, path, subpath, create = False)


class WikiPageFactory (object):
	# Обрабатываемый этой фабрикой тип страниц
	type = u"wiki"

	# Название страницы, показываемое пользователю
	title = _(u"Wiki Page")


	# Настройки
	# Показывать вкладку с HTML-кодом?
	showHtmlCodeOptions = BooleanOption (Application.config, "Wiki", "ShowHtmlCode", True)

	# Размер превьюшек по умолчанию
	thumbSizeOptions = IntegerOption (Application.config, "Wiki", "ThumbSize", 250)


	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		assert not title.startswith ("__")

		path = os.path.join (parent.path, title)
		page = WikiWikiPage.create (parent, path, title, WikiPageFactory.type, tags)
		return page


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


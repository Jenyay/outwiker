#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from core.tree import WikiPage, createPage
from HtmlPanel import HtmlPagePanel
import core.exceptions

class HtmlWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	
	@staticmethod
	def getType ():
		return u"html"


class HtmlPageFactory (object):
	@staticmethod
	def getPageType():
		return HtmlWikiPage

	@staticmethod
	def getTypeString ():
		return HtmlPageFactory.getPageType().getType()

	# Название страницы, показываемое пользователю
	title = _(u"HTML Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return createPage (HtmlPageFactory.getPageType(), parent, title, tags)


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = HtmlPagePanel (parent)
		panel.page = page

		return panel


	@staticmethod
	def getPrefPanels (parent):
		return []

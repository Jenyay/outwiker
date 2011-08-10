#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from core.tree import WikiPage
from HtmlPanel import HtmlPagePanel
from core.factory import PageFactory

class HtmlWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	
	@staticmethod
	def getTypeString ():
		return u"html"


class HtmlPageFactory (PageFactory):
	@staticmethod
	def getPageType():
		return HtmlWikiPage

	@staticmethod
	def getTypeString ():
		return HtmlPageFactory.getPageType().getTypeString()

	# Название страницы, показываемое пользователю
	title = _(u"HTML Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return PageFactory.createPage (HtmlPageFactory.getPageType(), parent, title, tags)


	@staticmethod
	def getPageView (parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = HtmlPagePanel (parent)

		return panel


	@staticmethod
	def getPrefPanels (parent):
		return []

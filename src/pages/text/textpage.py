#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

import os.path

from outwiker.core.tree import WikiPage
from pages.text.TextPanel import TextPanel
from outwiker.core.factory import PageFactory


class TextWikiPage (WikiPage):
	"""
	Класс текстовых страниц
	"""
	def __init__(self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	

	@staticmethod
	def getTypeString ():
		return u"text"


class TextPageFactory (PageFactory):
	@staticmethod
	def getPageType():
		return TextWikiPage

	@staticmethod
	def getTypeString ():
		return TextPageFactory.getPageType().getTypeString()

	# Название страницы, показываемое пользователю
	title = _(u"Text Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return PageFactory.createPage (TextPageFactory.getPageType(), parent, title, tags)


	@staticmethod
	def getPageView (parent):
		"""
		Вернуть контрол, котоырй будет отображать и редактировать страницу
		"""
		panel = TextPanel (parent)

		return panel


	@staticmethod
	def getPrefPanels (parent):
		return []


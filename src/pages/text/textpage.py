#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

import os.path

from core.tree import WikiPage
from pages.text.TextPanel import TextPanel

class TextWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__(self, path, title, parent):
		WikiPage.__init__ (self, path, title, parent)
	

	@staticmethod
	def getType ():
		return u"text"


class TextPageFactory (object):
	type = TextWikiPage.getType()

	# Название страницы, показываемое пользователю
	title = _(u"Text Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		assert not title.startswith ("__")

		path = os.path.join (parent.path, title)
		page = TextWikiPage.create (parent, path, title, TextWikiPage.getType(), tags)
		return page


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, котоырй будет отображать и редактировать страницу
		"""
		return TextPanel (page, parent)


	@staticmethod
	def getPrefPanels (parent):
		return []


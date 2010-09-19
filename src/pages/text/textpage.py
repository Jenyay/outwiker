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


class TextPageFactory (object):
	type = u"text"

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		assert not title.startswith ("__")

		path = os.path.join (parent.path, title)
		page = TextWikiPage.create (parent, path, title, TextPageFactory.type, tags)
		return page


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, котоырй будет отображать и редактировать страницу
		"""
		return TextPanel (page, parent)


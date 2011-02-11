#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from core.tree import WikiPage
from HtmlPanel import HtmlPagePanel

class HtmlWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, subpath, create = False):
		WikiPage.__init__ (self, path, subpath, create = False)
	
	@staticmethod
	def getType ():
		return u"html"


class HtmlPageFactory (object):
	type = HtmlWikiPage.getType()

	# Название страницы, показываемое пользователю
	title = _(u"HTML Page")

	def __init__ (self):
		pass

	@staticmethod
	def create (parent, title, tags):
		assert not title.startswith ("__")

		path = os.path.join (parent.path, title)
		page = HtmlWikiPage.create (parent, path, title, HtmlWikiPage.getType(), tags)
		return page


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

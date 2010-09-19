#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from core.tree import WikiPage
from wikipanel import WikiPagePanel

class WikiWikiPage (WikiPage):
	"""
	Класс wiki-страниц
	"""
	def __init__ (self, path, subpath, create = False):
		WikiPage.__init__ (self, path, subpath, create = False)


class WikiPageFactory (object):
	type = u"wiki"

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

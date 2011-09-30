#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from .exceptions import ReadonlyException

class PageFactory (object):
	"""
	Класс для создания страниц
	"""
	@staticmethod
	def createPage (pageType, parent, title, tags):
		"""
		Создать страницу по ее типу
		"""
		if parent.readonly:
			raise ReadonlyException

		path = os.path.join (parent.path, title)

		page = pageType (path, title, parent)
		parent.addToChildren (page)

		try:
			page.initAfterCreating (tags)
		except Exception:
			parent.removeFromChildren (page)
			raise

		return page


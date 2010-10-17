#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pages.text.textpage import TextPageFactory
from pages.html.htmlpage import HtmlPageFactory
from pages.search.searchpage import SearchPageFactory
from pages.wiki.wikipage import WikiPageFactory


class FactorySelector (object):
	"""
	Класс, который выбирает нужную фабрику для каждой страницы
	"""
	factories = [WikiPageFactory, 
			HtmlPageFactory, 
			TextPageFactory, 
			SearchPageFactory]

	defaultFactory = TextPageFactory

	def __init__ (self):
		pass

	@staticmethod
	def getFactory (page):
		"""
		Найти фабрику, которая работает с переданной страницей (до страницей данного типа).
		Или вернуть фабрику по умолчанию
		"""
		selFactory = FactorySelector.defaultFactory

		for factory in FactorySelector.factories:
			if page.type == factory.type:
				selFactory = factory
				break

		return selFactory


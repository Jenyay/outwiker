#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с поиском
"""

import os.path

from core.tree import WikiPage, createPage
from core.search import AllTagsSearchStrategy, AnyTagSearchStrategy, TagsList

from SearchPanel import SearchPanel
import core.system
from core.application import Application
import core.exceptions

paramsSection = u"Search"

class SearchWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	

	@staticmethod
	def getType ():
		return u"search"


class SearchPageFactory (object):
	@staticmethod
	def getPageType():
		return SearchWikiPage

	@staticmethod
	def getTypeString ():
		return SearchPageFactory.getPageType().getType()

	# Название страницы, показываемое пользователю
	title = _(u"Search Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return createPage (SearchPageFactory.getPageType(), parent, title, tags)


	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = SearchPanel (parent)
		panel.page = page

		return panel


	@staticmethod
	def getPrefPanels (parent):
		return []


class GlobalSearch (object):
	pageTitle = _(u"# Search")

	@staticmethod
	def create (root, phrase = u"", tags = [], strategy = AllTagsSearchStrategy):
		"""
		Создать страницу с поиском. Если страница существует, то сделать ее активной
		"""
		title = GlobalSearch.pageTitle
		number = 1
		page = None

		imagesDir = core.system.getImagesDir()

		while page == None:
			page = root[title]
			if page == None:
				page = SearchPageFactory.create (root, title, [])
				page.icon = os.path.join (imagesDir, "global_search.png")
			elif page.type != SearchPageFactory.getTypeString():
				number += 1
				title = u"%s %d" % (GlobalSearch.pageTitle, number)
				page = None

		setPhrase (page, phrase)
		setTags (page, [tag for tag in tags])
		setStrategy (page, strategy)
		page.root.selectedPage = page

		return page


def getPhrase (page):
	phrase = u""
	try:
		phrase = page.getParameter (paramsSection, u"phrase")
	except:
		pass
	return phrase


def setPhrase (page, phrase):
	page.setParameter (paramsSection, u"phrase", phrase)
	Application.onPageUpdate (page)


def getTags (page):
	"""
	Загрузить список тегов из настроек страницы
	"""
	tags_str = u""

	try:
		tags_str = page.getParameter (paramsSection, "tags")
	except:
		pass

	tags = TagsList.parseTagsList (tags_str)
	return tags


def setTags (page, tags):
	tags_str = TagsList.getTagsString (tags)
	page.setParameter (paramsSection, u"tags", tags_str)
	Application.onPageUpdate (page)


def getStrategy (page):
	strategy = 0
	try:
		strategy = int (page.getParameter (paramsSection, u"strategy"))
	except:
		pass

	#print "getStrategy: " + str (strategy)

	if strategy == 0:
		return AnyTagSearchStrategy
	else:
		return AllTagsSearchStrategy


def setStrategy (page, strategy):
	if strategy == AllTagsSearchStrategy:
		strategyCode = 1
	else:
		strategyCode = 0

	page.setParameter (paramsSection, u"strategy", strategyCode)
	Application.onPageUpdate (page)

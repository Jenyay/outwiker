#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с поиском
"""

import os.path

from core.tree import WikiPage
from core.search import AllTagsSearchStrategy, AnyTagSearchStrategy, TagsList

from SearchPanel import SearchPanel
from core.controller import Controller
import core.system

paramsSection = u"Search"

class SearchWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__ (self, path, subpath, create = False):
		WikiPage.__init__ (self, path, subpath, create = False)


class SearchPageFactory (object):
	type = u"search"

	def __init__ (self):
		pass

	@staticmethod
	def create (parent, title, tags):
		assert not title.startswith ("__")

		path = os.path.join (parent.path, title)
		page = SearchWikiPage.create (parent, path, title, SearchPageFactory.type, tags)
		return page

	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, который будет отображать и редактировать страницу
		"""
		panel = SearchPanel (parent)
		panel.page = page

		return panel


class GlobalSearch (object):
	pageTitle = u"# Search"

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
			elif page.type != SearchPageFactory.type:
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
	Controller.instance().onPageUpdate (page)


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
	Controller.instance().onPageUpdate (page)


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
	Controller.instance().onPageUpdate (page)


#def makeSearchPageWrapper (page):
#	"""
#	Добавить к странице методы для удобного доступа к свойствам поиска
#	"""
#
#	paramsSection = u"Search"
#	if page == None:
#		return None
#
#	def getPhrase (self):
#		phrase = u""
#		try:
#			phrase = self.getParameter (paramsSection, u"phrase")
#		except:
#			pass
#		return phrase
#
#
#	def setPhrase (self, phrase):
#		self.setParameter (paramsSection, u"phrase", phrase)
#		Controller.instance().onPageUpdate (self)
#
#	
#	def getTags (self):
#		"""
#		Загрузить список тегов из настроек страницы
#		"""
#		tags_str = u""
#
#		try:
#			tags_str = self.getParameter (paramsSection, "tags")
#		except:
#			pass
#
#		tags = TagsList.parseTagsList (tags_str)
#		return tags
#
#
#	def setTags (self, tags):
#		tags_str = TagsList.getTagsString (tags)
#		self.setParameter (paramsSection, u"tags", tags_str)
#		Controller.instance().onPageUpdate (self)
#	
#
#	def getStrategy (self):
#		strategy = 0
#		try:
#			strategy = int (self.getParameter (paramsSection, u"strategy"))
#		except:
#			pass
#
#		if strategy == 0:
#			return AllTagsSearchStrategy
#		else:
#			return AnyTagSearchStrategy
#
#
#	def setStrategy (self, strategy):
#		if strategy == AllTagsSearchStrategy:
#			strategyCode = 0
#		else:
#			strategyCode = 1
#
#		self.setParameter (paramsSection, u"strategy", strategyCode)
#		Controller.instance().onPageUpdate (self)
#
#
#	#page.searchPhrase = property (getPhrase, setPhrase)
#	#page.searchTags = property (getTags, setTags)
#	#page.searchStrategy = property (getStrategy, setStrategy)
#
#
#	page.getSearchPhrase = getPhrase
#	page.setSearchPhrase = setPhrase
#
#	page.getSearchTags = getTags
#	page.setSearchTags = setTags
#
#	page.getSearchStrategy = getStrategy
#	page.setSearchStrategy = setStrategy
#
#	#setattr (page.__class__, "searchPhrase", property (getPhrase, setPhrase))
#	#setattr (page.__class__, "searchTags", property (getTags, setTags))
#	#setattr (page.__class__, "searchStrategy", property (getStrategy, setStrategy))
#
#	return page
#
#

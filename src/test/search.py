#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from core.search import Searcher, TagsList, AllTagsSearchStrategy, \
		AnyTagSearchStrategy

from pages.search.searchpage import GlobalSearch
import pages.search.searchpage

from pages.search.searchpage import SearchPageFactory, SearchWikiPage
from test.utils import removeWiki
from core.tree import WikiDocument
from pages.text.textpage import TextPageFactory

class SearcherTest(unittest.TestCase):
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"page 1", [u"метка 1", u"Метка 2"])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
		TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 1", u"метка 2"])
		
		self.rootwiki[u"page 1"].content = ur"1  декабря. (Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
			утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

		self.rootwiki[u"page 1/page 5"].content = ur"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
			отчетливо слово 'пивная'"

		self.rootwiki[u"Страница 2"].content = ur"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
			Взвешивание  дало неожиданный  результат - 30 кг  за счет роста (удлинение)\
			костей. Пес по-прежнему лежит."

		self.rootwiki[u"Страница 2/Страница 3"].content = ur"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
			и на боках туловища."

		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = ur"2 Января. Фотографирован во время  улыбки при магнии. \
			Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."
	

	def testSearchContentAll (self):
		phrase = u"Декабря"
		tags = []

		searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 3)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)

	
	def testSearchContentAny (self):
		phrase = u"Декабря"
		tags = []

		searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 3)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)
	

	def testSearchAllAll (self):
		phrase = u""
		tags = []

		searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 5)

	
	def testSearchAllAny (self):
		phrase = u""
		tags = []

		searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 5)

	
	def testSearchSingleTagAll (self):
		phrase = u""
		tags = [u"Метка 1"]

		searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 4)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
		self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)

	
	def testSearchSingleTagAny (self):
		phrase = u""
		tags = [u"Метка 1"]

		searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 4)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
		self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
	

	def testSearchTag2All (self):
		phrase = u""
		tags = [u"МеткА 1", u"МетКа 2"]

		searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 2)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
	

	def testSearchTag2Any (self):
		phrase = u""
		tags = [u"МеткА 1", u"МетКа 3"]

		searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
		pages = searcher.find (self.rootwiki)

		self.assertEqual (len (pages), 4)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
		self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
	

	def testSearchFullAll (self):
		phrase = u"Декабря"
		tags = [u"Метка 2"]

		searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
		pages = searcher.find (self.rootwiki)
		
		self.assertEqual (len (pages), 2)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


	def testSearchFullAny (self):
		phrase = u"Декабря"
		tags = [u"Метка 2"]

		searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
		pages = searcher.find (self.rootwiki)
		
		self.assertEqual (len (pages), 2)
		self.assertTrue (self.rootwiki[u"page 1"] in pages)
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


class TagsListTest (unittest.TestCase):
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"page 1", [u"Метка 1", u"Метка 2"])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
		TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 4"])

	
	def test1 (self):
		tags = TagsList (self.rootwiki)

		self.assertEqual (len (tags), 4)

		self.assertEqual (len (tags[u"Метка 1"]), 3)
		self.assertTrue (self.rootwiki[u"page 1"] in tags[u"Метка 1"])
		self.assertTrue (self.rootwiki[u"Страница 2"] in tags[u"Метка 1"])
		self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in tags[u"Метка 1"])
	

	def testParseTags (self):
		tagsString = u" метка 1 , Метка 2, метка 3,, , "

		tags = TagsList.parseTagsList (tagsString)

		self.assertEqual (len (tags), 3)

		self.assertTrue (u"метка 1" in tags)
		self.assertTrue (u"Метка 2" in tags)
		self.assertTrue (u"метка 3" in tags)


class SearchPageTest (unittest.TestCase):
	"""
	Тест на создание страниц с поиском
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"page 1", [u"Метка 1", u"Метка 2"])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
		TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 4"])

		self.rootwiki[u"page 1"].content = ur"1  декабря. (Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
			утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

		self.rootwiki[u"page 1/page 5"].content = ur"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
			отчетливо слово 'пивная'"

		self.rootwiki[u"Страница 2"].content = ur"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
			Взвешивание  дало неожиданный  результат - 30 кг  за счет роста (удлинение)\
			костей. Пес по-прежнему лежит."

		self.rootwiki[u"Страница 2/Страница 3"].content = ur"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
			и на боках туловища."

		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = ur"2 Января. Фотографирован во время  улыбки при магнии. \
			Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."
	

	def testCreateDefaultPage (self):
		GlobalSearch.create (self.rootwiki)
		page = self.rootwiki[GlobalSearch.pageTitle]

		self.assertTrue (page != None)
		self.assertEqual (self.rootwiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase(page), u"")
		self.assertEqual (len (pages.search.searchpage.getTags(page) ), 0)
		self.assertEqual (pages.search.searchpage.getStrategy(page), AllTagsSearchStrategy)
	

	def testCreateSearchTagsPage (self):
		GlobalSearch.create (self.rootwiki, tags = [u"Метка 1", u"Метка 2"])
		page = self.rootwiki[GlobalSearch.pageTitle]

		self.assertTrue (page != None)
		self.assertEqual (self.rootwiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase(page), u"")
		self.assertEqual (len (pages.search.searchpage.getTags(page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page) )
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)
	

	def testCreateSearchPhrasePage (self):
		GlobalSearch.create (self.rootwiki, phrase = u"декабрь")
		page = self.rootwiki[GlobalSearch.pageTitle]

		self.assertTrue (page != None)
		self.assertEqual (self.rootwiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 0)
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)

	
	def testCreateSearchAllPage (self):
		GlobalSearch.create (self.rootwiki, 
				phrase = u"декабрь", 
				tags = [u"Метка 1", u"Метка 2"],
				strategy = AllTagsSearchStrategy)

		page = self.rootwiki[GlobalSearch.pageTitle]

		self.assertTrue (page != None)
		self.assertEqual (self.rootwiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page))
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)
	

	def testLoadSearchPage (self):
		GlobalSearch.create (self.rootwiki, 
				phrase = u"декабрь", 
				tags = [u"Метка 1", u"Метка 2"],
				strategy = AllTagsSearchStrategy)

		wiki = WikiDocument.load (self.path)
		page = wiki[GlobalSearch.pageTitle]

		self.assertTrue (page != None)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page))
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)
	

	def testManySearchPages1 (self):
		GlobalSearch.create (self.rootwiki)

		GlobalSearch.create (self.rootwiki, 
				phrase = u"декабрь", 
				tags = [u"Метка 1", u"Метка 2"],
				strategy = AllTagsSearchStrategy)

		wiki = WikiDocument.load (self.path)
		page = wiki[GlobalSearch.pageTitle]

		self.assertEqual (wiki[GlobalSearch.pageTitle + u" 2"], None)
		self.assertTrue (page != None)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page))
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)
	

	def testManySearchPages2 (self):
		TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle, [])

		GlobalSearch.create (self.rootwiki, 
				phrase = u"декабрь", 
				tags = [u"Метка 1", u"Метка 2"],
				strategy = AllTagsSearchStrategy)

		wiki = WikiDocument.load (self.path)
		page = wiki[GlobalSearch.pageTitle + u" 2"]

		self.assertTrue (page != None)
		#self.assertEqual (wiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page))
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)
	

	def testManySearchPages3 (self):
		TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle, [])
		TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 2", [])
		TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 3", [])
		TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 4", [])

		GlobalSearch.create (self.rootwiki, 
				phrase = u"декабрь", 
				tags = [u"Метка 1", u"Метка 2"],
				strategy = AllTagsSearchStrategy)

		wiki = WikiDocument.load (self.path)
		page = wiki[GlobalSearch.pageTitle + u" 5"]

		self.assertTrue (page != None)
		#self.assertEqual (wiki.selectedPage, page)
		self.assertEqual (pages.search.searchpage.getPhrase (page), u"декабрь")
		self.assertEqual (len (pages.search.searchpage.getTags (page)), 2)
		self.assertTrue (u"Метка 1" in pages.search.searchpage.getTags (page))
		self.assertTrue (u"Метка 2" in pages.search.searchpage.getTags (page))
		self.assertEqual (pages.search.searchpage.getStrategy (page), AllTagsSearchStrategy)


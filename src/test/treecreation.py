#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.config import StringOption
from outwiker.core.application import Application
from outwiker.core.exceptions import DublicateTitle
from outwiker.pages.text.textpage import TextPageFactory, TextWikiPage
from outwiker.pages.html.htmlpage import HtmlPageFactory, HtmlWikiPage
from outwiker.pages.search.searchpage import SearchPageFactory, SearchWikiPage
from outwiker.pages.wiki.wikipage import WikiPageFactory, WikiWikiPage
from test.utils import removeWiki


class TextPageCreationTest(unittest.TestCase):
	"""
	Класс тестов, связанных с созданием страниц вики
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)
		self.eventcount = 0

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

		self.rootwiki[u"Страница 1"].content = u"1234567"
		self.rootwiki[u"Страница 2/Страница 3"].content = u"Абырвалг"
		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = u"Тарам-пам-пам"
		self.rootwiki[u"Страница 1/Страница 5"].content = u"111111"

		self.rootwiki[u"Страница 1"].tags = [u"метка 1"]
		self.rootwiki[u"Страница 2/Страница 3"].tags = [u"метка 2", u"метка 3"]
		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags = [u"метка 1", u"метка 2", u"метка 4"]

		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].icon = "../test/images/feed.gif"

		self.icons = ["../test/images/icon.gif", 
				"../test/images/icon.png",
				"../test/images/icon.jpg",
				"../test/images/icon.ico"]

		Application.wikiroot = None


	def tearDown(self):
		Application.wikiroot = None
		removeWiki (self.path)


	def onPageUpdate (self, page):
		self.eventcount += 1


	def testEventChangeContent (self):
		Application.wikiroot = self.rootwiki
		Application.onPageUpdate += self.onPageUpdate

		self.rootwiki[u"Страница 1"].content = u"тарам-там-там"
		self.assertEqual (self.eventcount, 1)

		# То же самое содержимое
		self.rootwiki[u"Страница 1"].content = u"тарам-там-там"
		self.assertEqual (self.eventcount, 1)

		Application.onPageUpdate -= self.onPageUpdate


	def testNoEventChangeContent (self):
		Application.onPageUpdate += self.onPageUpdate

		self.rootwiki[u"Страница 1"].content = u"тарам-там-там"
		self.assertEqual (self.eventcount, 0)
		
		Application.onPageUpdate -= self.onPageUpdate


	def testEventChangeTags (self):
		Application.wikiroot = self.rootwiki
		Application.onPageUpdate += self.onPageUpdate

		self.rootwiki[u"Страница 1"].tags = [u"метка 1", u"метка 2", u"метка 4"]
		self.assertEqual (self.eventcount, 1)

		# То же самое содержимое
		self.rootwiki[u"Страница 1"].tags = [u"метка 1", u"метка 2", u"метка 4"]
		self.assertEqual (self.eventcount, 1)

		Application.onPageUpdate -= self.onPageUpdate


	def testNoEventChangeTags (self):
		Application.onPageUpdate += self.onPageUpdate

		self.rootwiki[u"Страница 1"].tags = [u"метка 1", u"метка 2", u"метка 4"]
		self.assertEqual (self.eventcount, 0)

		Application.onPageUpdate -= self.onPageUpdate


	def testAttach1 (self):
		# Получить путь до прикрепленных файлов, не создавая ее
		path = Attachment (self.rootwiki[u"Страница 2"]).getAttachPath()
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertFalse (os.path.exists (path))
	

	def testAttach2 (self):
		# Получить путь до прикрепленных файлов, не создавая ее
		path = Attachment (self.rootwiki[u"Страница 2"]).getAttachPath(create=False)
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertFalse (os.path.exists (path))

	def testAttach3 (self):
		# Получить путь до прикрепленных файлов, создав ее
		path = Attachment (self.rootwiki[u"Страница 2"]).getAttachPath(create=True)
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertTrue (os.path.exists (path))
	

	def testTypeCreation (self):
		textPage = TextPageFactory.create (self.rootwiki, u"Текстовая страница", [])
		self.assertEqual (TextWikiPage, type(textPage))

		wikiPage = WikiPageFactory.create (self.rootwiki, u"Вики-страница", [])
		self.assertEqual (WikiWikiPage, type(wikiPage))

		htmlPage = HtmlPageFactory.create (self.rootwiki, u"HTML-страница", [])
		self.assertEqual (HtmlWikiPage, type(htmlPage))

		searchPage = SearchPageFactory.create (self.rootwiki, u"Поисковая страница", [])
		self.assertEqual (SearchWikiPage, type(searchPage))


	def testIcon (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (os.path.basename (wiki[u"Страница 2/Страница 3/Страница 4"].icon), 
				"__icon.gif")


	def testReplaceIcon (self):
		wiki = WikiDocument.load (self.path)

		wiki[u"Страница 1"].icon = self.icons[3]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.ico")

		wiki[u"Страница 1"].icon = self.icons[1]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.png")

		wiki[u"Страница 1"].icon = self.icons[0]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.gif")

		wiki[u"Страница 1"].icon = self.icons[2]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.jpg")

		wiki[u"Страница 1"].icon = self.icons[3]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.ico")

		wiki[u"Страница 1"].icon = self.icons[0]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.gif")

		wiki[u"Страница 1"].icon = self.icons[1]
		self.assertEqual (os.path.basename (wiki[u"Страница 1"].icon), "__icon.png")


	def testTags (self):
		wiki = WikiDocument.load (self.path)
		self.assertTrue (u"метка 1" in wiki[u"Страница 1"].tags)
		self.assertEqual (len (wiki[u"Страница 1"].tags), 1)

		self.assertTrue (u"метка 2" in wiki[u"Страница 2/Страница 3"].tags)
		self.assertTrue (u"метка 3" in wiki[u"Страница 2/Страница 3"].tags)
		self.assertEqual (len (wiki[u"Страница 2/Страница 3"].tags), 2)

		self.assertTrue (u"метка 1" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertTrue (u"метка 2" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertTrue (u"метка 4" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertEqual (len (wiki[u"Страница 2/Страница 3/Страница 4"].tags), 3)



	def testCreation (self):
		self.assertTrue (os.path.exists (self.path))
		self.assertTrue (os.path.exists (os.path.join (self.path, RootWikiPage.pageConfig) ) )


	def testInvalidPageName (self):
		children = len (self.rootwiki.children)
		self.assertRaises (Exception, TextPageFactory.create, self.rootwiki, u"+*5name:/\0", [])
		self.assertEqual (len (self.rootwiki.children), children)
	

	def testInvalidPageName2 (self):
		self.assertRaises (DublicateTitle, 
				TextPageFactory.create, self.rootwiki, u"страНица 1", [])

		self.assertRaises (DublicateTitle, 
				TextPageFactory.create, self.rootwiki[u"Страница 1"], u"страНица 5", [])


	def testPageCreate (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].title, u"Страница 1")
		self.assertEqual (wiki[u"Страница 2"].title, u"Страница 2")
		self.assertEqual (wiki[u"Страница 2/Страница 3"].title, u"Страница 3")
	

	def testCreateTextContent (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].content, u"1234567")
		self.assertEqual (wiki[u"Страница 2/Страница 3"].content, u"Абырвалг")
		self.assertEqual (wiki[u"Страница 2/Страница 3/Страница 4"].content, u"Тарам-пам-пам")
		self.assertEqual (wiki[u"Страница 1/Страница 5"].content, u"111111")
	

	def testLastViewedPage1 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		wiki = WikiDocument.load (self.path)
		section = u"History"
		param = u"LastViewedPage"

		subpath = StringOption (wiki.params, section, param, u"")

		wiki.selectedPage = wiki[u"Страница 1"]
		self.assertEqual (subpath.value, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		self.assertEqual (subpath.value, u"Страница 2/Страница 3")

		# Проверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath2 = StringOption (wiki2.params, section, param, u"")
		self.assertEqual (subpath2.value, u"Страница 2/Страница 3")

	
	def testLastViewedPage2 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		wiki = WikiDocument.load (self.path)

		self.assertEqual (wiki.lastViewedPage, None)

		wiki.selectedPage = wiki[u"Страница 1"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")

		# Проверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath = wiki2.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")


	def testLastViewedPage3 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]

		self.rootwiki.selectedPage = self.rootwiki

		# Проверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		#subpath = wiki2.lastViewedPage
		self.assertEqual (wiki2.selectedPage, None)


	def testSelection1 (self):
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
		self.assertEqual (self.rootwiki.selectedPage, self.rootwiki[u"Страница 2/Страница 3"])


	def testSelection2 (self):
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
		wiki2 = WikiDocument.load (self.path)

		self.assertEqual (wiki2.selectedPage, wiki2[u"Страница 2/Страница 3"])


	def testSelection3 (self):
		self.rootwiki.selectedPage = None
		wiki2 = WikiDocument.load (self.path)

		self.assertEqual (wiki2.selectedPage, None)


	def testSelection4 (self):
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
		self.rootwiki[u"Страница 2/Страница 3"].remove()

		wiki2 = WikiDocument.load (self.path)

		self.assertEqual (wiki2.selectedPage, wiki2[u"Страница 2"])


	def testSelection5 (self):
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
		self.rootwiki[u"Страница 2"].remove()

		wiki2 = WikiDocument.load (self.path)

		self.assertEqual (wiki2.selectedPage, None)


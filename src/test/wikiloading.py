#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument

from pages.text.textpage import TextPageFactory, TextWikiPage
from pages.wiki.wikipage import WikiPageFactory, WikiWikiPage
from pages.html.htmlpage import HtmlPageFactory, HtmlWikiPage
from pages.search.searchpage import SearchPageFactory, SearchWikiPage

from core.event import Event
from core.application import Application
from test.utils import removeWiki


class WikiPagesTest(unittest.TestCase):
	"""
	Тест на открытие вики
	"""
	def setUp(self):
		self.path = u"../test/samplewiki"
		self.root = WikiDocument.load (self.path)


	def testLoadWiki(self):
		self.assertEqual ( len (self.root), 5, "Pages count == 5")


	def testPagesAccess (self):
		"""
		Проверка доступа к отдельным страницам и правильности установки заголовков
		"""
		self.assertEqual (self.root[u"page 4"].title, u"page 4")
		self.assertEqual (self.root[u"Страница 1"].title, u"Страница 1")
		self.assertEqual (self.root[u"стрАниЦа 3"].title, u"Страница 3")
		self.assertEqual (self.root[u"Страница 1/Страница 2"].title, u"Страница 2")
		self.assertEqual (self.root[u"СтраНица 1/стРаниЦА 2/СтраНицА 5"].title, u"Страница 5")
		self.assertEqual (self.root[u"Страница 1"][u"Страница 2"].title, u"Страница 2")

		self.assertEqual (self.root[u"Страница 111"], None)
	

	def testPageType1 (self):
		self.assertEqual (type (self.root[u"Типы страниц/HTML-страница"]), HtmlWikiPage)
		self.assertEqual (type (self.root[u"Типы страниц/wiki-страница"]), WikiWikiPage)
		self.assertEqual (type (self.root[u"Типы страниц/Страница поиска"]), SearchWikiPage)
		self.assertEqual (type (self.root[u"Типы страниц/Текстовая страница"]), TextWikiPage)
	

	def testPageType2 (self):
		self.assertEqual (self.root[u"Типы страниц/HTML-страница"].getTypeString(), 
				HtmlWikiPage.getTypeString())

		self.assertEqual (self.root[u"Типы страниц/wiki-страница"].getTypeString(), 
				WikiWikiPage.getTypeString())

		self.assertEqual (self.root[u"Типы страниц/Страница поиска"].getTypeString(), 
				SearchWikiPage.getTypeString())

		self.assertEqual (self.root[u"Типы страниц/Текстовая страница"].getTypeString(), 
				TextWikiPage.getTypeString())


	def testPagesParent (self):
		"""
		Проверка доступа к отдельным страницам и правильности установки заголовков
		"""
		self.assertEqual (self.root[u"page 4"].parent, self.root)
		self.assertEqual (self.root[u"Страница 1"].parent, self.root)
		self.assertEqual (self.root[u"Страница 1/Страница 2"].parent, self.root[u"Страница 1"])
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].parent, self.root[u"Страница 1/Страница 2"])

		self.assertEqual (self.root.parent, None)


	def testPagesPath (self):
		"""
		Проверка правильности путей до страниц
		"""
		self.assertEqual (self.root[u"page 4"].path, os.path.join (self.path, u"page 4") )
		self.assertEqual (self.root[u"Страница 1"].path, os.path.join (self.path, u"Страница 1") )
		self.assertEqual (self.root[u"Страница 3"].path, os.path.join (self.path, u"Страница 3") )

		fullpath = os.path.join (self.path, u"Страница 1")
		fullpath = os.path.join (fullpath, u"Страница 2")

		self.assertEqual (self.root[u"Страница 1/Страница 2"].path, fullpath)



	def testTags (self):
		self.assertTrue (u"Тест" in self.root[u"Страница 1"].tags)
		self.assertTrue (u"test" in self.root[u"Страница 1"].tags, self.root[u"Страница 1"].tags)
		self.assertTrue (u"двойной тег" in self.root[u"Страница 1"].tags)
		self.assertEqual (len (self.root[u"Страница 1"].tags), 3)

		self.assertTrue (u"test" in self.root[u"Страница 1/Страница 2"].tags)
		self.assertEqual (len (self.root[u"Страница 1/Страница 2"].tags), 1)

		self.assertTrue (u"test" in self.root[u"Страница 3"].tags)
		self.assertTrue (u"тест" in self.root[u"Страница 3"].tags)
		self.assertEqual (len (self.root[u"Страница 3"].tags), 2)

		self.assertEqual (len (self.root[u"page 4"].tags), 0)


	def testTypes (self):
		self.assertEqual (self.root[u"Страница 1"].getTypeString(), "html")
		self.assertEqual (self.root[u"Страница 1/Страница 2"].getTypeString(), "text")
		self.assertEqual (self.root[u"Страница 3"].getTypeString(), "html")
		self.assertEqual (self.root[u"page 4"].getTypeString(), "text")
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].getTypeString(), "text")


	def testChildren (self):
		self.assertEqual (len (self.root[u"Страница 1"].children), 1)
		self.assertEqual (self.root[u"Страница 1"].children[0], self.root[u"Страница 1/Страница 2"])

		self.assertEqual (len (self.root[u"Страница 1/Страница 2"].children), 1)
		self.assertEqual (len (self.root[u"Страница 3"].children), 0)
		self.assertEqual (len (self.root[u"page 4"].children), 0)


	def testIcons (self):
		self.assertEqual (os.path.basename (self.root[u"Страница 1"].icon), "__icon.png")
		self.assertEqual (os.path.basename (self.root[u"Страница 1/Страница 2"].icon), "__icon.gif")
		self.assertEqual (self.root[u"Страница 3"].icon, None)


	def testParams (self):
		self.assertEqual (self.root[u"Страница 1"].getParameter (u"General", u"type"), u"html")
		self.assertEqual (self.root[u"Страница 1"].getParameter (u"General", u"tags"), u"Тест, test, двойной тег")
		

	def testGetRoot (self):
		self.assertEqual (self.root[u"Страница 1"].root, self.root)
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].root, self.root)
	

	def testSubpath (self):
		self.assertEqual (self.root[u"Страница 1"].subpath, u"Страница 1")

		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].subpath, 
				u"Страница 1/Страница 2/Страница 5")



class SubWikiTest (unittest.TestCase):
	"""
	Тест на открытие подстраниц вики как полноценную вики
	"""
	def setUp (self):
		self.rootpath = u"../test/samplewiki"

	def test1 (self):
		path = os.path.join (self.rootpath, u"Страница 1")
		root = WikiDocument.load (path)

		self.assertEqual ( len (root), 1)
		self.assertEqual ( root[u"Страница 2"].title, u"Страница 2")


class TextPageAttachmentTest (unittest.TestCase):
	"""
	Тест для проверки работы с прикрепленными файлами
	"""
	def setUp (self):
		# Количество срабатываний особытий при обновлении страницы
		self.pageUpdateCount = 0
		self.pageUpdateSender = None

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

	def tearDown(self):
		removeWiki (self.path)


	def testEvent (self):
		self.pageUpdateCount = 0

		Application.onPageUpdate += self.onPageUpdate

		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		
		self.assertEqual (self.pageUpdateCount, 1)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page1])

		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )
		
		self.assertEqual (self.pageUpdateCount, 2)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page3])

		Application.onPageUpdate -= self.onPageUpdate


	def onPageUpdate (self, sender):
		self.pageUpdateCount += 1
		self.pageUpdateSender = sender


	def testAttach (self):
		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )

		# Заново загрузим вики
		wiki = WikiDocument.load (self.path)

		# Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
		self.assertEqual (len (wiki[page1].attachment), 3)
		self.assertEqual (len (wiki[page3].attachment), 2)
		self.assertEqual (len (wiki[u"Страница 2"].attachment), 0)

		# Проверим пути до прикрепленных файлов
		attachPathPage1 = TextPageAttachmentTest.getFullAttachPath (wiki, page1, files)
		attachPathPage3 = TextPageAttachmentTest.getFullAttachPath (wiki, page3, files)

		#print attachPathPage1
		#print wiki[page1].attachment
		self.assertTrue (attachPathPage1[0] in wiki[page1].attachment)
		self.assertTrue (attachPathPage1[1] in wiki[page1].attachment)
		self.assertTrue (attachPathPage1[2] in wiki[page1].attachment)
		
		self.assertTrue (attachPathPage3[0] in wiki[page3].attachment)
		self.assertTrue (attachPathPage3[1] in wiki[page3].attachment)


	def testAttach2 (self):
		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )

		# Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
		self.assertEqual (len (self.rootwiki[page1].attachment), 3)
		self.assertEqual (len (self.rootwiki[page3].attachment), 2)
		self.assertEqual (len (self.rootwiki[u"Страница 2"].attachment), 0)

		# Проверим пути до прикрепленных файлов
		attachPathPage1 = TextPageAttachmentTest.getFullAttachPath (self.rootwiki, page1, files)
		attachPathPage3 = TextPageAttachmentTest.getFullAttachPath (self.rootwiki, page3, files)

		#print attachPathPage1
		#print wiki[page1].attachment
		self.assertTrue (attachPathPage1[0] in self.rootwiki[page1].attachment)
		self.assertTrue (attachPathPage1[1] in self.rootwiki[page1].attachment)
		self.assertTrue (attachPathPage1[2] in self.rootwiki[page1].attachment)
		
		self.assertTrue (attachPathPage3[0] in self.rootwiki[page3].attachment)
		self.assertTrue (attachPathPage3[1] in self.rootwiki[page3].attachment)


	@staticmethod
	def getFullAttachPath (wiki, pageSubpath, fnames):
		"""
		Сформировать список полных путей до прикрепленных файлов
		wiki -- загруженная вики
		pageSubpath -- путь до страницы
		fnames -- имена файлов
		"""
		attachPath = os.path.join (wiki[pageSubpath].getAttachPath())
		result = [os.path.join (attachPath, fname) for fname in fnames]

		return result




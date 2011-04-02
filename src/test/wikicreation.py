#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import shutil
import unittest
import stat

from core.tree import RootWikiPage, WikiDocument

from pages.text.textpage import TextPageFactory, TextWikiPage
from pages.html.htmlpage import HtmlPageFactory, HtmlWikiPage
from pages.search.searchpage import SearchPageFactory, SearchWikiPage
from pages.wiki.wikipage import WikiPageFactory, WikiWikiPage
from core.attachment import Attachment

from core.event import Event
from core.application import Application
from test.utils import removeWiki
import core.exceptions


class TextPageCreationTest(unittest.TestCase):
	"""
	Класс тестов, связанных с созданием страниц вики
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

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

	def tearDown(self):
		removeWiki (self.path)
	

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
		self.assertRaises (core.exceptions.DublicateTitle, 
				TextPageFactory.create, self.rootwiki, u"страНица 1", [])

		self.assertRaises (core.exceptions.DublicateTitle, 
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

		wiki.selectedPage = wiki[u"Страница 1"]
		subpath = wiki.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		subpath = wiki.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 2/Страница 3")

		# Прверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath = wiki2.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 2/Страница 3")

	
	def testLastViewedPage1 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		wiki = WikiDocument.load (self.path)
		section = u"History"
		param = u"LastViewedPage"

		self.assertEqual (wiki.lastViewedPage, None)

		wiki.selectedPage = wiki[u"Страница 1"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")

		# Прверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath = wiki2.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")



class ConfigPagesTest (unittest.TestCase):
	"""
	Тесты, связанные с настройками страниц и вики в целом
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])

		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])


	def testSetRootParams (self):
		self.rootwiki.setParameter (u"TestSection_1", u"value1", u"Значение 1")

		self.assertEqual (self.rootwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.create (self.path)
		self.assertEqual (wiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")


	def testSetPageParams (self):
		self.rootwiki[u"Страница 1"].setParameter (u"TestSection_1", u"value1", u"Значение 1")

		self.assertEqual (self.rootwiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")


	def testSubwikiParams (self):
		"""
		Проверка того, что установка параметров страницы как полноценной вики не портит исходные параметры
		"""
		self.rootwiki[u"Страница 1"].setParameter (u"TestSection_1", u"value1", u"Значение 1")

		path = os.path.join (self.path, u"Страница 1")
		subwiki = WikiDocument.load (path)
		
		self.assertEqual (subwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")

		# Добавим новый параметр
		subwiki.setParameter (u"TestSection_2", u"value2", u"Значение 2")
		
		self.assertEqual (subwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")
		self.assertEqual (subwiki.getParameter (u"TestSection_2", u"value2"), u"Значение 2")

		# На всякий случай прочитаем вики еще раз
		wiki = WikiDocument.load (self.path)
		
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")
		
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_2", u"value2"), 
				u"Значение 2")


class BookmarksTest (unittest.TestCase):
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

		self.bookmarkCount = 0
		self.bookmarkSender = None


	def onBookmark (self, bookmarks):
		self.bookmarkCount += 1
		self.bookmarkSender = bookmarks
	

	def testAddToBookmarks (self):
		# По умолчанию закладок нет
		self.assertEqual (len (self.rootwiki.bookmarks), 0)

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

		self.assertEqual (len (self.rootwiki.bookmarks), 1)
		self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")

		# Проверим, что закладки сохраняются в конфиг
		wiki = WikiDocument.load (self.path)

		self.assertEqual (len (wiki.bookmarks), 1)
		self.assertEqual (wiki.bookmarks[0].title, u"Страница 1")
	

	def testManyBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.assertEqual (len (self.rootwiki.bookmarks), 3)
		self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
		self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2")
		self.assertEqual (self.rootwiki.bookmarks[2].subpath, u"Страница 2/Страница 3")
	

	def testRemoveBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])

		self.assertEqual (len (self.rootwiki.bookmarks), 2)
		self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
		self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2/Страница 3")
	

	def testBookmarkEvent (self):
		Application.onBookmarksChanged += self.onBookmark

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.assertEqual (self.bookmarkCount, 1)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.assertEqual (self.bookmarkCount, 2)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)


		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])
		self.assertEqual (self.bookmarkCount, 3)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)
	

	def testPageInBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1"]), 
				True)

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 2/Страница 3"]),
				True)

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1/Страница 5"]), 
				False)
	

	def testCloneBookmarks (self):
		"""
		Тест на повторное добавление одной и той же страницы
		"""
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

		self.assertEqual (len (self.rootwiki.bookmarks), 1)
		self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")


class RemovePagesTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.treeUpdateCount = 0
		self.pageRemoveCount = 0


	def onTreeUpdate (self, bookmarks):
		"""
		Обработка события при удалении страницы (обновление дерева)
		"""
		self.treeUpdateCount += 1

	
	def onPageRemove (self, bookmarks):
		"""
		Обработка события при удалении страницы
		"""
		self.pageRemoveCount += 1

	
	def testRemove1 (self):
		Application.onTreeUpdate += self.onTreeUpdate
		Application.onPageRemove += self.onPageRemove

		# Удаляем страницу из корня
		page6 = self.rootwiki[u"Страница 6"]
		page6.remove()
		self.assertEqual (len (self.rootwiki), 2)
		self.assertEqual (self.rootwiki[u"Страница 6"], None)
		self.assertTrue (page6.isRemoved)
		self.assertEqual (self.pageRemoveCount, 1)

		# Удаляем подстраницу
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		page3.remove()

		self.assertEqual (len (self.rootwiki[u"Страница 2"]), 0)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3"], None)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3/Страница 4"], None)
		self.assertTrue (page3.isRemoved)
		self.assertTrue (page4.isRemoved)
		self.assertEqual (self.pageRemoveCount, 3)
		
		Application.onTreeUpdate -= self.onTreeUpdate
		Application.onPageRemove -= self.onPageRemove
	

	def testIsRemoved (self):
		"""
		Провкерка свойства isRemoved
		"""
		page6 = self.rootwiki[u"Страница 6"]
		page6.remove()
		self.assertTrue (page6.isRemoved)

		# Удаляем подстраницу
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		page3.remove()

		self.assertTrue (page3.isRemoved)
		self.assertTrue (page4.isRemoved)

		self.assertFalse (self.rootwiki[u"Страница 2"].isRemoved)

	def testRemoveSelectedPage1 (self):
		"""
		Удаление выбранной страницы
		"""
		# Если удаляется страница из корня, то никакая страница не выбирается
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 6"]
		self.rootwiki[u"Страница 6"].remove()

		self.assertEqual (self.rootwiki.selectedPage, None)

		# Если удаляется страница более глубокая, то выбранной страницей становится родитель
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		self.rootwiki.selectedPage.remove()
		self.assertEqual (self.rootwiki.selectedPage, self.rootwiki[u"Страница 2/Страница 3"])
	

	def testRemoveSelectedPage2 (self):
		"""
		Удаление выбранной страницы
		"""
		# Если удаляется страница более глубокая, то выбранной страницей становится родитель
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		self.rootwiki.selectedPage.remove()
		self.assertEqual (self.rootwiki.selectedPage, self.rootwiki[u"Страница 2/Страница 3"])


	def testRemoveFromBookmarks1 (self):
		"""
		Проверка того, что страница удаляется из закладок
		"""
		page = self.rootwiki[u"Страница 6"]
		self.rootwiki.bookmarks.add (page)
		page.remove()

		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page))
	

	def testRemoveFromBookmarks2 (self):
		"""
		Проверка того, что подстраница удаленной страницы удаляется из закладок
		"""
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		self.rootwiki.bookmarks.add (page2)
		self.rootwiki.bookmarks.add (page3)
		self.rootwiki.bookmarks.add (page4)

		page2.remove()

		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page2))
		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page3))
		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page4))


class RenameTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.treeUpdateCount = 0

	
	def testRename1 (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"Страница 1 new"

		self.assertEqual (page.title, u"Страница 1 new")
		self.assertEqual (self.rootwiki[u"Страница 1 new"], page)
		self.assertEqual (page.subpath, u"Страница 1 new")
		self.assertEqual (self.rootwiki[u"Страница 1"], None)

	
	def testInvalidRename (self):
		def rename (page, newtitle):
			page.title = newtitle

		self.assertRaises (core.exceptions.DublicateTitle, rename, 
				self.rootwiki[u"Страница 1"], u"СтраНица 6")
	

	def testRename2 (self):
		page = self.rootwiki[u"Страница 2/Страница 3"]
		page.title = u"Страница 3 new"

		self.assertEqual (page.title, u"Страница 3 new")
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3 new"], page)
		self.assertEqual (page.subpath, u"Страница 2/Страница 3 new")
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3"], None)
	

	def testRename3 (self):
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = page3[u"Страница 4"]

		page3.title = u"Страница 3 new"

		self.assertEqual (page3[u"Страница 4"], page4)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3 new/Страница 4"], page4)
	

	def testRename4 (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"СтрАницА 1"

		self.assertEqual (page.title, u"СтрАницА 1")
		self.assertEqual (self.rootwiki[u"СтрАницА 1"], page)
		self.assertEqual (page.subpath, u"СтрАницА 1")

	
	def testLoad (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"Страница 1 new"

		wiki = WikiDocument.load (self.path)
		self.assertNotEqual (wiki[u"Страница 1 new"], None)
		self.assertEqual (wiki[u"Страница 1"], None)
	

	def testBookmarks1 (self):
		page = self.rootwiki[u"Страница 6"]
		self.rootwiki.bookmarks.add (page)
		page.title = u"Страница 6 new"

		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page))
	

	def testBookmarks2 (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		self.rootwiki.bookmarks.add (page2)
		self.rootwiki.bookmarks.add (page3)
		self.rootwiki.bookmarks.add (page4)

		page2.title = u"Страница 2 new"

		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page2))
		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page3))
		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page4))
	

	def testPath (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		page2.title = u"Страница 2 new"

		self.assertEqual (page2.path, os.path.join (self.path, u"Страница 2 new"))
		self.assertEqual (page3.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3"))
		self.assertEqual (page4.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3", u"Страница 4"))
	

	def testConfig (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		page2.title = u"Страница 2 new"

		page2.tags = [u"тег 1"]
		page3.tags = [u"тег 2"]
		page4.tags = [u"тег 3"]

		self.assertEqual (page2.tags[0], u"тег 1")
		self.assertEqual (page3.tags[0], u"тег 2")
		self.assertEqual (page4.tags[0], u"тег 3")


	def testRenameError (self):
		page = self.rootwiki[u"Страница 2"]
		attach = Attachment (page)
		path = attach.getAttachPath (True)
		os.chmod (page.path, stat.S_IREAD)

		try:
			page.title = u"Новое имя"
		except IOError:
			pass
		else:
			self.fail()
		finally:
			os.chmod (page.path, stat.S_IWRITE | stat.S_IREAD | stat.S_IRWXU)


#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from core.tree import RootWikiPage, WikiDocument

from pages.text.textpage import TextPageFactory, TextWikiPage

from core.application import Application
from test.utils import removeWiki


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

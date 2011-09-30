#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты обработки событий
"""

import os.path
import shutil
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from pages.html.htmlpage import HtmlPageFactory
from outwiker.core.event import Event
from outwiker.core.application import Application
from test.utils import removeWiki


class EventTest (unittest.TestCase):
	def setUp (self):
		self.value1 = 0
		self.value2 = 0
		self.value3 = 0

	def event1 (self):
		self.value1 = 1

	def event2 (self, param):
		self.value2 = 2

	def event3 (self, param):
		self.value3 = 3

	def testAdd1 (self):
		event = Event()
		event += self.event1

		event()

		self.assertEqual (self.value1, 1)
		self.assertEqual (self.value2, 0)


	def testAdd2 (self):
		event = Event()
		event += self.event2

		event(111)

		self.assertEqual (self.value1, 0)
		self.assertEqual (self.value2, 2)


	def testAdd3 (self):
		event = Event()
		event += self.event2
		event += self.event3

		event(111)

		self.assertEqual (self.value2, 2)
		self.assertEqual (self.value3, 3)


	def testRemove1 (self):
		event = Event()
		event += self.event1
		event -= self.event1

		event()

		self.assertEqual (self.value1, 0)

	def testRemove2 (self):
		event = Event()
		event += self.event2
		event += self.event3
		event -= self.event2

		event(111)

		self.assertEqual (self.value2, 0)
		self.assertEqual (self.value3, 3)


class EventsTest (unittest.TestCase):
	def setUp (self):
		Application.wikiroot = None
		self.path = u"../test/testwiki"

		self.isPageUpdate = False
		self.isPageCreate = False
		self.isTreeUpdate = False
		self.isPageSelect = False
		
		self.pageUpdateSender = None
		self.pageCreateSender = None
		self.treeUpdateSender = None
		self.pageSelectSender = None

		self.pageUpdateCount = 0
		self.pageCreateCount = 0
		self.treeUpdateCount = 0
		self.pageSelectCount = 0

		Application.wikiroot = None

	def tearDown(self):
		Application.wikiroot = None
		removeWiki (self.path)

	def pageUpdate (self, sender):
		self.isPageUpdate = True
		self.pageUpdateSender = sender
		self.pageUpdateCount += 1

	def pageCreate(self, sender):
		self.isPageCreate = True
		self.pageCreateSender = sender
		self.pageCreateCount += 1

	def treeUpdate (self, sender):
		self.isTreeUpdate = True
		self.treeUpdateSender = sender
		self.treeUpdateCount += 1

	def pageSelect (self, sender):
		self.isPageSelect = True
		self.pageSelectSender = sender
		self.pageSelectCount += 1


	def testLoad (self):
		path = u"../test/samplewiki"
		Application.onTreeUpdate += self.treeUpdate

		self.assertFalse(self.isTreeUpdate)
		root = WikiDocument.load (path)

		self.assertFalse (self.isTreeUpdate)
		self.assertEqual (self.treeUpdateSender, None)
		self.assertEqual (self.treeUpdateCount, 0)

		Application.onTreeUpdate -= self.treeUpdate


	def testCreateEvent (self):
		Application.onTreeUpdate += self.treeUpdate
		Application.onPageCreate += self.pageCreate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertEqual (self.treeUpdateSender, None)

		Application.wikiroot = rootwiki

		# Создаем страницу верхнего уровня (не считая корня)
		self.isPageCreate = False
		self.pageCreateSender = None

		TextPageFactory.create (rootwiki, u"Страница 1", [])
		
		self.assertTrue(self.isPageCreate)
		self.assertEqual (self.pageCreateSender, rootwiki[u"Страница 1"])

		# Создаем еще одну страницу
		self.isPageCreate = False
		self.pageCreateSender = None

		TextPageFactory.create (rootwiki, u"Страница 2", [])

		self.assertTrue(self.isPageCreate)
		self.assertEqual (self.pageCreateSender, rootwiki[u"Страница 2"])

		# Создаем подстраницу
		self.isPageCreate = False
		self.pageCreateSender = None

		TextPageFactory.create (rootwiki[u"Страница 2"], u"Страница 3", [])

		self.assertTrue(self.isPageCreate)
		self.assertEqual (self.pageCreateSender, rootwiki[u"Страница 2/Страница 3"])

		Application.onTreeUpdate -= self.treeUpdate
		Application.onPageCreate -= self.pageCreate


	def testCreateNoEvent (self):
		Application.onTreeUpdate += self.treeUpdate
		Application.onPageCreate += self.pageCreate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertEqual (self.treeUpdateSender, None)

		# Создаем страницу верхнего уровня (не считая корня)
		self.isPageCreate = False
		self.pageCreateSender = None

		TextPageFactory.create (rootwiki, u"Страница 1", [])
		
		self.assertFalse(self.isPageCreate)
		self.assertEqual (self.pageCreateSender, None)


	def testUpdateContentEvent (self):
		"""
		Тест на срабатывание событий при обновлении контента
		"""
		Application.onPageUpdate += self.pageUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		Application.wikiroot = rootwiki

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].content = "1111"
		
		self.assertTrue(self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, rootwiki[u"Страница 1"])

		Application.onPageUpdate -= self.pageUpdate
		Application.wikiroot = None


	def testUpdateContentNoEvent (self):
		"""
		Тест на НЕсрабатывание событий при обновлении контента
		"""
		Application.onPageUpdate += self.pageUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].content = "1111"
		
		self.assertFalse(self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, None)

		Application.onPageUpdate -= self.pageUpdate


	def testUpdateTagsEvent (self):
		"""
		Тест на срабатывание событий при обновлении меток (тегов)
		"""
		Application.onPageUpdate += self.pageUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		Application.wikiroot = rootwiki

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].tags = ["test"]
		
		self.assertTrue(self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, rootwiki[u"Страница 1"])

		Application.onPageUpdate -= self.pageUpdate


	def testUpdateTagsNoEvent (self):
		"""
		Тест на срабатывание событий при обновлении меток (тегов)
		"""
		Application.onPageUpdate += self.pageUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].tags = ["test"]
		
		self.assertFalse(self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, None)

		Application.onPageUpdate -= self.pageUpdate


	def testUpdateIcon (self):
		"""
		Тест на срабатывание событий при обновлении иконки
		"""
		Application.onPageUpdate += self.pageUpdate
		Application.onTreeUpdate += self.treeUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		Application.wikiroot = rootwiki

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].icon = "../test/images/feed.gif"
		
		self.assertTrue (self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, rootwiki[u"Страница 1"])
		
		self.assertTrue (self.isTreeUpdate)
		self.assertEqual (self.treeUpdateSender, rootwiki[u"Страница 1"])

		Application.onPageUpdate -= self.pageUpdate
		Application.onTreeUpdate -= self.treeUpdate


	def testUpdateIconNoEvent (self):
		"""
		Тест на НЕсрабатывание событий при обновлении иконки, если не устанолен Application.wikiroot
		"""
		Application.wikiroot = None

		Application.onPageUpdate += self.pageUpdate
		Application.onTreeUpdate += self.treeUpdate

		removeWiki (self.path)

		self.assertFalse(self.isTreeUpdate)
		self.assertFalse(self.isPageUpdate)
		self.assertFalse(self.isPageCreate)

		# Создаем вики
		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])

		Application.wikiroot = rootwiki

		# Изменим содержимое страницы
		rootwiki[u"Страница 1"].icon = "../test/images/feed.gif"
		
		self.assertTrue (self.isPageUpdate)
		self.assertEqual (self.pageUpdateSender, rootwiki[u"Страница 1"])
		
		self.assertTrue (self.isTreeUpdate)
		self.assertEqual (self.treeUpdateSender, rootwiki[u"Страница 1"])

		Application.onPageUpdate -= self.pageUpdate
		Application.onTreeUpdate -= self.treeUpdate


	def testPageSelectCreate (self):
		Application.onPageSelect += self.pageSelect

		removeWiki (self.path)

		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])
		TextPageFactory.create (rootwiki, u"Страница 2", [])
		TextPageFactory.create (rootwiki[u"Страница 2"], u"Страница 3", [])

		Application.wikiroot = rootwiki

		self.assertEqual (rootwiki.selectedPage, None)

		rootwiki.selectedPage = rootwiki[u"Страница 1"]
		
		self.assertEqual (rootwiki.selectedPage, rootwiki[u"Страница 1"])
		self.assertEqual (self.isPageSelect, True)
		self.assertEqual (self.pageSelectSender, rootwiki[u"Страница 1"])
		self.assertEqual (self.pageSelectCount, 1)

		rootwiki.selectedPage = rootwiki[u"Страница 2/Страница 3"]

		self.assertEqual (rootwiki.selectedPage, rootwiki[u"Страница 2/Страница 3"])
		self.assertEqual (self.isPageSelect, True)
		self.assertEqual (self.pageSelectSender, rootwiki[u"Страница 2/Страница 3"])
		self.assertEqual (self.pageSelectCount, 2)

		Application.onPageSelect -= self.pageSelect


	def testPageSelectCreateNoEvent (self):
		Application.onPageSelect += self.pageSelect

		removeWiki (self.path)

		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])
		TextPageFactory.create (rootwiki, u"Страница 2", [])
		TextPageFactory.create (rootwiki[u"Страница 2"], u"Страница 3", [])

		Application.wikiroot = rootwiki

		self.assertEqual (rootwiki.selectedPage, None)

		rootwiki.selectedPage = rootwiki[u"Страница 1"]
		
		self.assertEqual (rootwiki.selectedPage, rootwiki[u"Страница 1"])
		self.assertEqual (self.isPageSelect, True)


	def testPageSelectLoad (self):
		Application.onPageSelect += self.pageSelect

		removeWiki (self.path)

		rootwiki = WikiDocument.create (self.path)
		TextPageFactory.create (rootwiki, u"Страница 1", [])
		TextPageFactory.create (rootwiki, u"Страница 2", [])
		TextPageFactory.create (rootwiki[u"Страница 2"], u"Страница 3", [])

		document = WikiDocument.load (self.path)
		Application.wikiroot = document

		self.assertEqual (document.selectedPage, None)

		document.selectedPage = document[u"Страница 1"]
		
		self.assertEqual (document.selectedPage, document[u"Страница 1"])
		self.assertEqual (self.isPageSelect, True)
		self.assertEqual (self.pageSelectSender, document[u"Страница 1"])
		self.assertEqual (self.pageSelectCount, 1)

		document.selectedPage = document[u"Страница 2/Страница 3"]

		self.assertEqual (document.selectedPage, document[u"Страница 2/Страница 3"])
		self.assertEqual (self.isPageSelect, True)
		self.assertEqual (self.pageSelectSender, document[u"Страница 2/Страница 3"])
		self.assertEqual (self.pageSelectCount, 2)

		Application.onPageSelect -= self.pageSelect

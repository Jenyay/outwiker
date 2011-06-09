#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Тесты порядка сортировки страниц
"""

import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument, WikiPage
from pages.text.textpage import TextPageFactory
from core.event import Event
from core.application import Application
from test.utils import removeWiki
from core.config import PageConfig

class PageOrderTest (unittest.TestCase):
	"""
	Тесты порядка сортировки страниц
	"""
	def setUp (self):
		# Количество срабатываний особытий при изменении порядка страниц
		self.orderUpdateCount = 0
		self.orderUpdateSender = None

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)
		Application.onPageOrderChange += self.onPageOrder

	
	def tearDown(self):
		Application.onPageOrderChange -= self.onPageOrder
		removeWiki (self.path)
	

	def onPageOrder (self, sender):
		self.orderUpdateCount += 1
		self.orderUpdateSender = sender

	
	def testFirstPage (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (len (self.rootwiki.children), 1)
		self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
	

	def testCreateOrder1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

		self.assertEqual (len (self.rootwiki.children), 2)
		self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])
	

	def testCreateOrder2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)

		self.assertEqual (len (self.rootwiki.children), 3)
		self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])
		self.assertEqual (self.rootwiki.children[2], self.rootwiki[u"Страница 3"])

	
	def testCreateOrder3 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

		self.assertEqual (len (self.rootwiki.children), 2)
		self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])
	

	def testCreateOrder4 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 7", [])

		self.rootwiki[u"Страница 7"].order = 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 4)
	

	def testCreateOrder5 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 7", [])

		self.rootwiki[u"Страница 7"].order = 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

		TextPageFactory.create (self.rootwiki, u"Страница 8", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)
		self.assertEqual (self.rootwiki[u"Страница 8"].order, 4)
	

	def testCreateOrder6 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 7", [])

		self.rootwiki[u"Страница 7"].order = 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 4)


	def testCreateOrder7 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 7", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])

		self.rootwiki[u"Страница 7"].order = 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)
		self.assertEqual (self.rootwiki[u"Страница 6"].order, 4)
	

	def testChangeOrder1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 4"].order += 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)


	def testChangeOrder2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вверх,хотя страница и так в самом верху
		self.rootwiki[u"Страница 1"].order -= 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)
	

	def testChangeOrder3 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 4"].order -= 1

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)
	

	def testChangeOrder4 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 4"].order -= 2

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)
	

	def testChangeOrder5 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 2"].order += 2

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)
	

	def testChangeOrder6 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 2"].order = 0

		self.assertEqual (self.rootwiki[u"Страница 2"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 1"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)
	

	def testChangeOrder7 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 2"].order = 3

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)
	

	def testChangeOrder8 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 2"].order = 100

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)
	

	def testChangeOrder9 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		self.rootwiki[u"Страница 4"].order = -100

		self.assertEqual (self.rootwiki[u"Страница 4"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 1"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)

	
	def testEventOrder1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 4"].order += 1

		self.assertEqual (self.orderUpdateCount, 1)
		self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 4"])
	

	def testEventOrder2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вверх,хотя страница и так в самом верху
		self.rootwiki[u"Страница 1"].order -= 1

		self.assertEqual (self.orderUpdateCount, 1)
		self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])
	

	def testEventOrder3 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 1"].order += 1

		self.assertEqual (self.orderUpdateCount, 1)
		self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])
	

	def testEventOrder4 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 1"].order += 2

		self.assertEqual (self.orderUpdateCount, 1)
		self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])


	def testEventOrder5 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 1"].order = 2

		self.assertEqual (self.orderUpdateCount, 1)
		self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])
	

	def testLoading1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 0", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])

		wikiroot = WikiDocument.load (self.path)

		self.assertEqual (wikiroot[u"Страница 0"].order, 0)
		self.assertEqual (wikiroot[u"Страница 1"].order, 1)
		self.assertEqual (wikiroot[u"Страница 2"].order, 2)
		self.assertEqual (wikiroot[u"Страница 3"].order, 3)
	

	def testLoading2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 0", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])

		self.rootwiki[u"Страница 0"].order += 1

		wikiroot = WikiDocument.load (self.path)

		self.assertEqual (wikiroot[u"Страница 1"].order, 0)
		self.assertEqual (wikiroot[u"Страница 0"].order, 1)
		self.assertEqual (wikiroot[u"Страница 2"].order, 2)
		self.assertEqual (wikiroot[u"Страница 3"].order, 3)
	

	def testLoading3 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 0", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])

		self.rootwiki[u"Страница 0"].order += 1
		self.rootwiki[u"Страница 3"].order -= 1

		wikiroot = WikiDocument.load (self.path)

		self.assertEqual (wikiroot[u"Страница 1"].order, 0)
		self.assertEqual (wikiroot[u"Страница 0"].order, 1)
		self.assertEqual (wikiroot[u"Страница 3"].order, 2)
		self.assertEqual (wikiroot[u"Страница 2"].order, 3)
	

	def testLoadingOldVersion1 (self):
		"""
		Тест на чтение вики старой версии, когда еще не было параметра order
		"""
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 0", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		# Удалим параметры order
		self.rootwiki[u"Страница 0"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 1"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 2"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 3"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)

		wikiroot = WikiDocument.load (self.path)

		self.assertEqual (wikiroot[u"Страница 0"].order, 0)
		self.assertEqual (wikiroot[u"Страница 1"].order, 1)
		self.assertEqual (wikiroot[u"Страница 2"].order, 2)
		self.assertEqual (wikiroot[u"Страница 3"].order, 3)
	

	def testLoadingOldVersion2 (self):
		"""
		Тест на чтение вики старой версии, когда еще не было параметра order
		"""
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 0", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		# Удалим параметры order
		self.rootwiki[u"Страница 0"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 1"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 2"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)
		self.rootwiki[u"Страница 3"].params.remove_option (PageConfig.sectionName, PageConfig.orderParamName)

		wikiroot = WikiDocument.load (self.path)

		self.assertEqual (wikiroot[u"Страница 0"].order, 0)
		self.assertEqual (wikiroot[u"Страница 1"].order, 1)
		self.assertEqual (wikiroot[u"Страница 2"].order, 2)
		self.assertEqual (wikiroot[u"Страница 3"].order, 3)

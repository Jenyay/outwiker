#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Тесты порядка сортировки страниц
"""

import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from core.event import Event
from core.controller import Controller
from core.factory import FactorySelector
from test.utils import removeWiki

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
		Controller.instance().onPageOrderChange -= self.onPageOrder

	
	def tearDown(self):
		removeWiki (self.path)
	

	def onPageOrder (self, sender):
		self.orderUpdateCount += 1
		self.orderUpdateSender = sender

	
	def testFirstPage (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (len (self.rootwiki.sortchildren), 1)
		self.assertEqual (self.rootwiki.sortchildren[0], self.rootwiki[u"Страница 1"])
	

	def testCreateOrder1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

		self.assertEqual (len (self.rootwiki.sortchildren), 2)
		self.assertEqual (self.rootwiki.sortchildren[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.sortchildren[1], self.rootwiki[u"Страница 2"])
	

	def testCreateOrder2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)

		self.assertEqual (len (self.rootwiki.sortchildren), 3)
		self.assertEqual (self.rootwiki.sortchildren[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.sortchildren[1], self.rootwiki[u"Страница 2"])
		self.assertEqual (self.rootwiki.sortchildren[2], self.rootwiki[u"Страница 3"])

	
	def testCreateOrder3 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

		self.assertEqual (len (self.rootwiki.sortchildren), 2)
		self.assertEqual (self.rootwiki.sortchildren[0], self.rootwiki[u"Страница 1"])
		self.assertEqual (self.rootwiki.sortchildren[1], self.rootwiki[u"Страница 2"])
	

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

		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
		self.assertEqual (self.rootwiki[u"Страница 6"].order, 1)
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
		self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
		self.assertEqual (self.rootwiki[u"Страница 1"].order, 2)
		self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)

	
	def testEventOrder1 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вниз,хотя страница и так в самом низу
		self.rootwiki[u"Страница 4"].order += 1

		self.assertEqual (self.orderUpdateCount, 0)
		self.assertEqual (self.orderUpdateSender, None)
	

	def testEventOrder2 (self):
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki, u"Страница 3", [])
		TextPageFactory.create (self.rootwiki, u"Страница 4", [])

		# Перемещаем вверх,хотя страница и так в самом верху
		self.rootwiki[u"Страница 1"].order -= 1

		self.assertEqual (self.orderUpdateCount, 0)
		self.assertEqual (self.orderUpdateSender, None)
	

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

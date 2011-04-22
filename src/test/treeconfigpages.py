#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import unittest

from core.tree import RootWikiPage, WikiDocument

from pages.text.textpage import TextPageFactory

from test.utils import removeWiki


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

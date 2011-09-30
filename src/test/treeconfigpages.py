#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.config import StringOption
from pages.text.textpage import TextPageFactory
from .utils import removeWiki


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
		param = StringOption (self.rootwiki.params, u"TestSection_1", u"value1", u"")
		param.value = u"Значение 1"

		self.assertEqual (param.value, u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.create (self.path)

		param_new = StringOption (wiki.params, u"TestSection_1", u"value1", u"")
		self.assertEqual (param_new.value, u"Значение 1")


	def testSetPageParams (self):
		param = StringOption (self.rootwiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
		param.value = u"Значение 1"

		param2 = StringOption (self.rootwiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
		self.assertEqual (param.value, u"Значение 1")
		self.assertEqual (param2.value, u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.load (self.path)
		param3 = StringOption (wiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")

		self.assertEqual (param3.value, u"Значение 1")


	def testSubwikiParams (self):
		"""
		Проверка того, что установка параметров страницы как полноценной вики не портит исходные параметры
		"""
		param = StringOption (self.rootwiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
		param.value = u"Значение 1"

		path = os.path.join (self.path, u"Страница 1")
		subwiki = WikiDocument.load (path)
		
		subwikiparam = StringOption (subwiki.params, u"TestSection_1", u"value1", u"")
		self.assertEqual (subwikiparam.value, u"Значение 1")

		# Добавим новый параметр
		subwikiparam1 = StringOption (subwiki.params, u"TestSection_1", u"value1", u"")
		subwikiparam2 = StringOption (subwiki.params, u"TestSection_2", u"value2", u"")
		subwikiparam2.value = u"Значение 2"
		
		self.assertEqual (subwikiparam1.value, u"Значение 1")
		self.assertEqual (subwikiparam2.value, u"Значение 2")

		# На всякий случай прочитаем вики еще раз
		wiki = WikiDocument.load (self.path)

		wikiparam1 = StringOption (wiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
		wikiparam2 = StringOption (wiki[u"Страница 1"].params, u"TestSection_2", u"value2", u"")
		
		self.assertEqual (wikiparam1.value, u"Значение 1")
		self.assertEqual (wikiparam2.value, u"Значение 2")

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты для проверки фабрик страниц
"""

import os.path
import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from pages.html.htmlpage import HtmlPageFactory
from core.event import Event
from core.factory import FactorySelector

class FactorySelectorTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/samplewiki"
		self.root = WikiDocument.load (self.path)

	def testSelection (self):
		self.assertEqual (FactorySelector.getFactory (self.root [u"Страница 1"].type), HtmlPageFactory)
		self.assertEqual (FactorySelector.getFactory (self.root [u"Страница 1/Страница 2"].type), TextPageFactory)
		self.assertEqual (FactorySelector.getFactory (self.root [u"Еще одна страница"].type), TextPageFactory)



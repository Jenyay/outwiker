#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты для проверки фабрик страниц
"""

import os.path
import shutil
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.core.event import Event
from outwiker.core.factoryselector import FactorySelector

class FactorySelectorTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/samplewiki"
		self.root = WikiDocument.load (self.path)

	def testSelection (self):
		self.assertEqual (FactorySelector.getFactory (self.root [u"Страница 1"].getTypeString()), HtmlPageFactory)
		self.assertEqual (FactorySelector.getFactory (self.root [u"Страница 1/Страница 2"].getTypeString()), TextPageFactory)
		self.assertEqual (FactorySelector.getFactory (self.root [u"Еще одна страница"].getTypeString()), TextPageFactory)



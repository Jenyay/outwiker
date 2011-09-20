#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import unittest

from core.tree import RootWikiPage, WikiDocument

from pages.html.htmlpage import HtmlPageFactory, HtmlWikiPage
from core.application import Application
from test.utils import removeWiki


class HtmlPagesTest(unittest.TestCase):
	"""
	Тесты HTML-страниц
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.__eventcount = 0
		self.__eventSender = None

		self.rootwiki = WikiDocument.create (self.path)

		HtmlPageFactory.create (self.rootwiki, u"Страница 1", [])
		HtmlPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.rootwiki.onPageUpdate += self.__onPageUpdate


	def tearDown(self):
		self.rootwiki.onPageUpdate -= self.__onPageUpdate
		removeWiki (self.path)


	def __onPageUpdate (self, sender):
		self.__eventcount += 1
		self.__eventSender = sender


	def testAutoLineWrap (self):
		self.assertTrue (self.rootwiki[u"Страница 1"].autoLineWrap)
		
		self.rootwiki[u"Страница 1"].autoLineWrap = False
		self.assertFalse (self.rootwiki[u"Страница 1"].autoLineWrap)


	def testAutoLineWrapReload (self):
		self.rootwiki[u"Страница 1"].autoLineWrap = False
		self.assertFalse (self.rootwiki[u"Страница 1"].autoLineWrap)

		wiki = WikiDocument.load (self.path)
		self.assertFalse (wiki[u"Страница 1"].autoLineWrap)


	def testAutoLineWrapRename (self):
		self.rootwiki[u"Страница 1"].autoLineWrap = False
		self.rootwiki[u"Страница 1"].title = u"Страница 666"
		self.assertFalse (self.rootwiki[u"Страница 666"].autoLineWrap)

		wiki = WikiDocument.load (self.path)
		self.assertFalse (wiki[u"Страница 666"].autoLineWrap)


	def testLineWrapEvent (self):
		self.rootwiki[u"Страница 1"].autoLineWrap = False

		self.assertEqual (self.__eventcount, 1)
		self.assertEqual (self.__eventSender, self.rootwiki[u"Страница 1"])



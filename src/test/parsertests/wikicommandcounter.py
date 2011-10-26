#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeWiki


class WikiCounterCommandTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"
		self.__createWiki()

		dirlist = [u"../plugins/testcounter"]

		self.loader = PluginsLoader(Application)
		self.loader.load (dirlist)
		
		self.factory = ParserFactory()
		self.parser = self.factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
		self.testPage = self.rootwiki[u"Страница 1"]
		

	def tearDown(self):
		removeWiki (self.path)


	def testPluginLoad (self):
		self.assertEqual ( len (self.loader), 1)


	def testCounter (self):
		text = u"(:counter:) (:counter:)"
		validResult = u"1 2"

		result = self.parser.toHtml (text)
		self.assertEqual (result, validResult)

		# Проверим, что для нового парсера счетчик сбрасывается
		parser2 = self.factory.make (self.testPage, Application.config)

		result2 = parser2.toHtml (text)
		self.assertEqual (result2, validResult)

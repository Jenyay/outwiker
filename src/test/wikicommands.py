#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from core.tree import WikiDocument
from core.application import Application
from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parser.command import Command
from pages.wiki.parserfactory import ParserFactory
from utils import removeWiki


class WikiCommandsTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"
		self.__createWiki()
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		self.testPage = self.rootwiki[u"Страница 2"]
		

	def tearDown(self):
		removeWiki (self.path)


	def testParamsParsing1 (self):
		params_text = u"""Параметр1 Параметр2 = 111 Параметр3 = " бла бла бла" Параметр4 Параметр5="111" Параметр6=' 222 ' Параметр7 = " проверка 'бла бла бла' проверка" Параметр8 = ' проверка "bla-bla-bla" тест ' """

		params = Command.parseParams (params_text)

		self.assertEqual (len (params), 8)
		self.assertEqual (params[u"Параметр1"], u"")
		self.assertEqual (params[u"Параметр2"], u"111")
		self.assertEqual (params[u"Параметр3"], u" бла бла бла")
		self.assertEqual (params[u"Параметр4"], u"")
		self.assertEqual (params[u"Параметр5"], u"111")
		self.assertEqual (params[u"Параметр6"], u" 222 ")
		self.assertEqual (params[u"Параметр7"], u" проверка 'бла бла бла' проверка")
		self.assertEqual (params[u"Параметр8"], u' проверка "bla-bla-bla" тест ')


	def testParamsParsing2 (self):
		params_text = u""
		params = Command.parseParams (params_text)

		self.assertEqual (len (params), 0)


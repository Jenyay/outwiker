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


class CounterTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/counter"]

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


    def testCounter_01 (self):
        text = u"(:counter:)"
        validResult = u"1"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)

        # Проверим, что для нового парсера счетчик сбрасывается
        parser2 = self.factory.make (self.testPage, Application.config)

        result2 = parser2.toHtml (text)
        self.assertEqual (result2, validResult)


    def testCounter_02 (self):
        text = u"(:counter:) (:counter:)"
        validResult = u"1 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)

        # Проверим, что для нового парсера счетчик сбрасывается
        parser2 = self.factory.make (self.testPage, Application.config)

        result2 = parser2.toHtml (text)
        self.assertEqual (result2, validResult)


    def testName_01 (self):
        text = u'(:counter name="Абырвалг":) (:counter name="Абырвалг":)'
        validResult = u"1 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_02 (self):
        text = u'(:counter name="Абырвалг":) (:counter:)'
        validResult = u"1 1"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_03 (self):
        text = u'(:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг":)'
        validResult = u"1 1 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_04 (self):
        text = u'(:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг":) (:counter:)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_05 (self):
        text = u'(:counter name="Абырвалг":) (:counter name:) (:counter name="Абырвалг":) (:counter name:)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_06 (self):
        text = u'(:counter name="Абырвалг":) (:counter name="":) (:counter name="Абырвалг":) (:counter name="":)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_07 (self):
        text = u'(:counter name="Абырвалг":) (:counter name="Новый счетчик":) (:counter name="Абырвалг":) (:counter name="Новый счетчик":)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_08 (self):
        text = u'(:counter name=" Абырвалг":) (:counter name="Новый счетчик ":) (:counter name="Абырвалг":) (:counter name="Новый счетчик":)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testName_09 (self):
        text = u'(:counter name="  Абырвалг":) (:counter name="Новый счетчик  ":) (:counter name=" Абырвалг ":) (:counter name="Новый счетчик ":)'
        validResult = u"1 1 2 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_01 (self):
        text = u"(:counter:) (:counter:) (:counter start=1:) (:counter:)"
        validResult = u"1 2 1 2"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_02 (self):
        text = u"(:counter start=5:) (:counter:) (:counter:)"
        validResult = u"5 6 7"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_03 (self):
        text = u"(:counter:) (:counter:) (:counter start=0:) (:counter:)"
        validResult = u"1 2 0 1"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_04 (self):
        text = u'(:counter:) (:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг" start=10:) (:counter:)'
        validResult = u"1 1 2 10 3"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_05 (self):
        text = u'(:counter start="-1":) (:counter:) (:counter:) (:counter start=10:)'
        validResult = u"-1 0 1 10"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)

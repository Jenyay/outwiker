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


    def testStart_06 (self):
        text = u'(:counter start="абырвалг":) (:counter:) (:counter:)'
        validResult = u"1 2 3"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStart_07 (self):
        text = u'(:counter:) (:counter:) (:counter start="абырвалг":)'
        validResult = u"1 2 3"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)




    def testParent_01 (self):
        text = u'''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)'''

        validResult = u'''1
1.1
1.2
1.3'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testParent_02 (self):
        text = u'''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 3" parent="level 2":)
(:counter name="level 3" parent="level 2":)'''

        validResult = u'''1
1.1
1.1.1
1.1.2'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testParent_03 (self):
        text = u'''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)'''

        validResult = u'''1
1.1
2
2.1
2.2'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testParent_04 (self):
        text = u'''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 3" parent="level 2":)
(:counter name="level 3" parent="level 2":)

(:counter name="level 2" parent="level 1":)
(:counter name="level 3" parent="level 2":)
(:counter name="level 3" parent="level 2":)

(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 3" parent="level 2":)
(:counter name="level 3" parent="level 2":)'''

        validResult = u'''1
1.1
1.1.1
1.1.2

1.2
1.2.1
1.2.2

2
2.1
2.1.1
2.1.2'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testInvalidParent_01 (self):
        text = u'''(:counter name="level 1" parent="level 1":)'''

        validResult = u'''1'''
        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testInvalidParent_02 (self):
        text = u'''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 1" parent="level 2":)
(:counter name="level 2" parent="level 1":)'''

        validResult = u'''1
1.1
1.1.1
1.1.1.1'''
        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testInvalidParent_03 (self):
        text = u'''(:counter name="level 1" parent="invalid":)
(:counter name="level 1" parent="invalid":)'''

        validResult = u'''1
2'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testFull_01 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)'''


        validResult = u'''Раздел 1
Раздел 2
Раздел 2.1
Раздел 2.1.1
Раздел 2.1.2
Раздел 2.1.3
Раздел 2.2
Раздел 2.3
Раздел 2.3.1
Раздел 2.3.2
Раздел 2.3.3
Раздел 2.3.3.1
Раздел 2.3.3.2
Раздел 2.3.3.3
Раздел 3
Раздел 3.1
Раздел 3.2
Раздел 3.3'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testFull_02 (self):
        text = u'''Раздел (:counter:)
Раздел (:counter:)
Раздел (:counter name="level 2" parent="":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 2" parent="":)
Раздел (:counter name="level 2" parent="":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 3" parent="level 2":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter name="level 4" parent="level 3":)
Раздел (:counter:)
Раздел (:counter name="level 2" parent="":)
Раздел (:counter name="level 2" parent="":)
Раздел (:counter name="level 2" parent="":)'''


        validResult = u'''Раздел 1
Раздел 2
Раздел 2.1
Раздел 2.1.1
Раздел 2.1.2
Раздел 2.1.3
Раздел 2.2
Раздел 2.3
Раздел 2.3.1
Раздел 2.3.2
Раздел 2.3.3
Раздел 2.3.3.1
Раздел 2.3.3.2
Раздел 2.3.3.3
Раздел 3
Раздел 3.1
Раздел 3.2
Раздел 3.3'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testFull_03 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10:)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = u'''Раздел 1
Раздел 1.1
Раздел 1.2
Раздел 1.10
Раздел 1.11'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testFull_04 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10:)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = u'''Раздел 1
Раздел 1.10
Раздел 1.11
Раздел 1.12
Раздел 1.13'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testHide_01 (self):
        text = u'''(:counter hide:)'''

        validResult = u''''''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testHide_02 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" hide:)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10 hide:)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = u'''Раздел 1
Раздел 1.1
Раздел 
Раздел 1.3
Раздел 
Раздел 1.11'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testHide_03 (self):
        text = u'''(:counter start=100 hide:)(:counter:)'''

        validResult = u'''101'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_01 (self):
        text = u'''(:counter:) (:counter step=2:)'''

        validResult = u'''1 3'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_02 (self):
        text = u'''(:counter step=2:)'''

        validResult = u'''2'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_03 (self):
        text = u'''(:counter step=2:) (:counter step=3:) (:counter step=4:)'''

        validResult = u'''2 5 9'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_04 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" step=2:)
Раздел (:counter name="level 2" parent="level 1" step=2:)'''

        validResult = u'''Раздел 1
Раздел 1.2
Раздел 1.4'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_05 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10 step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)'''

        validResult = u'''Раздел 1
Раздел 1.10
Раздел 1.110
Раздел 1.210
Раздел 1.310'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testStep_06 (self):
        text = u'''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=0:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)'''

        validResult = u'''Раздел 1
Раздел 1.0
Раздел 1.-100
Раздел 1.-200
Раздел 1.-300'''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)

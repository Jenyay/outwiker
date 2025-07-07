# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class CounterTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self._application = Application()

        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()

        dirlist = ["plugins/counter"]

        self.loader = PluginsLoader(self._application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self._application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testCounter_01(self):
        text = "(:counter:)"
        validResult = "1"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

        # Проверим, что для нового парсера счетчик сбрасывается
        parser2 = self.factory.make(self.testPage, self._application)

        result2 = parser2.toHtml(text)
        self.assertEqual(result2, validResult)

    def testCounter_02(self):
        text = "(:counter:) (:counter:)"
        validResult = "1 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

        # Проверим, что для нового парсера счетчик сбрасывается
        parser2 = self.factory.make(self.testPage, self._application)

        result2 = parser2.toHtml(text)
        self.assertEqual(result2, validResult)

    def testAlign_01(self):
        text = "%center%(:counter:)"
        validResult = '<div align="center">1</div>'

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testAlign_02(self):
        text = "%center%Рисунок (:counter:)."
        validResult = '<div align="center">Рисунок 1.</div>'

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testAlign_03(self):
        text = "%center%Рисунок (:counter:).\nqqq"
        validResult = '<div align="center">Рисунок 1.\nqqq</div>'

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testAlign_04(self):
        text = "%center%Рисунок (:counter:).\n\nqqq"
        validResult = '<div align="center">Рисунок 1.</div>\n\nqqq'

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testAlign_05(self):
        text = "%center%Рисунок (:counter:). (:counter:).\n\nqqq"
        validResult = '<div align="center">Рисунок 1. 2.</div>\n\nqqq'

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_01(self):
        text = '(:counter name="Абырвалг":) (:counter name="Абырвалг":)'
        validResult = "1 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_02(self):
        text = '(:counter name="Абырвалг":) (:counter:)'
        validResult = "1 1"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_03(self):
        text = '(:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг":)'
        validResult = "1 1 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_04(self):
        text = '(:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг":) (:counter:)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_05(self):
        text = '(:counter name="Абырвалг":) (:counter name:) (:counter name="Абырвалг":) (:counter name:)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_06(self):
        text = '(:counter name="Абырвалг":) (:counter name="":) (:counter name="Абырвалг":) (:counter name="":)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_07(self):
        text = '(:counter name="Абырвалг":) (:counter name="Новый счетчик":) (:counter name="Абырвалг":) (:counter name="Новый счетчик":)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_08(self):
        text = '(:counter name=" Абырвалг":) (:counter name="Новый счетчик ":) (:counter name="Абырвалг":) (:counter name="Новый счетчик":)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testName_09(self):
        text = '(:counter name="  Абырвалг":) (:counter name="Новый счетчик  ":) (:counter name=" Абырвалг ":) (:counter name="Новый счетчик ":)'
        validResult = "1 1 2 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_01(self):
        text = "(:counter:) (:counter:) (:counter start=1:) (:counter:)"
        validResult = "1 2 1 2"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_02(self):
        text = "(:counter start=5:) (:counter:) (:counter:)"
        validResult = "5 6 7"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_03(self):
        text = "(:counter:) (:counter:) (:counter start=0:) (:counter:)"
        validResult = "1 2 0 1"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_04(self):
        text = '(:counter:) (:counter name="Абырвалг":) (:counter:) (:counter name="Абырвалг" start=10:) (:counter:)'
        validResult = "1 1 2 10 3"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_05(self):
        text = '(:counter start="-1":) (:counter:) (:counter:) (:counter start=10:)'
        validResult = "-1 0 1 10"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_06(self):
        text = '(:counter start="абырвалг":) (:counter:) (:counter:)'
        validResult = "1 2 3"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStart_07(self):
        text = '(:counter:) (:counter:) (:counter start="абырвалг":)'
        validResult = "1 2 3"

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testParent_01(self):
        text = '''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)'''

        validResult = '''1
1.1
1.2
1.3'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testParent_02(self):
        text = '''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 3" parent="level 2":)
(:counter name="level 3" parent="level 2":)'''

        validResult = '''1
1.1
1.1.1
1.1.2'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testParent_03(self):
        text = '''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 2" parent="level 1":)'''

        validResult = '''1
1.1
2
2.1
2.2'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testParent_04(self):
        text = '''(:counter name="level 1":)
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

        validResult = '''1
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

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testInvalidParent_01(self):
        text = '''(:counter name="level 1" parent="level 1":)'''

        validResult = '''1'''
        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testInvalidParent_02(self):
        text = '''(:counter name="level 1":)
(:counter name="level 2" parent="level 1":)
(:counter name="level 1" parent="level 2":)
(:counter name="level 2" parent="level 1":)'''

        validResult = '''1
1.1
1.1.1
1.1.1.1'''
        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testInvalidParent_03(self):
        text = '''(:counter name="level 1" parent="invalid":)
(:counter name="level 1" parent="invalid":)'''

        validResult = '''1
2'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testFull_01(self):
        text = '''Раздел (:counter name="level 1":)
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

        validResult = '''Раздел 1
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

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testFull_02(self):
        text = '''Раздел (:counter:)
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

        validResult = '''Раздел 1
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

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testFull_03(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10:)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = '''Раздел 1
Раздел 1.1
Раздел 1.2
Раздел 1.10
Раздел 1.11'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testFull_04(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10:)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = '''Раздел 1
Раздел 1.10
Раздел 1.11
Раздел 1.12
Раздел 1.13'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testHide_01(self):
        text = '''(:counter hide:)'''

        validResult = ''''''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testHide_02(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" hide:)
Раздел (:counter name="level 2" parent="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10 hide:)
Раздел (:counter name="level 2" parent="level 1":)'''

        validResult = '''Раздел 1
Раздел 1.1
Раздел 
Раздел 1.3
Раздел 
Раздел 1.11'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testHide_03(self):
        text = '''(:counter start=100 hide:)(:counter:)'''

        validResult = '''101'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_01(self):
        text = '''(:counter:) (:counter step=2:)'''

        validResult = '''1 3'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_02(self):
        text = '''(:counter step=2:)'''

        validResult = '''2'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_03(self):
        text = '''(:counter step=2:) (:counter step=3:) (:counter step=4:)'''

        validResult = '''2 5 9'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_04(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" step=2:)
Раздел (:counter name="level 2" parent="level 1" step=2:)'''

        validResult = '''Раздел 1
Раздел 1.2
Раздел 1.4'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_05(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=10 step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)
Раздел (:counter name="level 2" parent="level 1" step="100":)'''

        validResult = '''Раздел 1
Раздел 1.10
Раздел 1.110
Раздел 1.210
Раздел 1.310'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_06(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" start=0:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)
Раздел (:counter name="level 2" parent="level 1" step=-100:)'''

        validResult = '''Раздел 1
Раздел 1.0
Раздел 1.-100
Раздел 1.-200
Раздел 1.-300'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testStep_07(self):
        text = '''(:counter start=0 step=2:)'''

        validResult = '''0'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testSeparator_01(self):
        text = '''Раздел (:counter name="level 1":)
Раздел (:counter name="level 2" parent="level 1" separator="/":)
Раздел (:counter name="level 2" parent="level 1" separator="/":)
Раздел (:counter name="level 2" parent="level 1" separator="/":)'''

        validResult = '''Раздел 1
Раздел 1/1
Раздел 1/2
Раздел 1/3'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testSeparator_02(self):
        text = '''Раздел (:counter:)
Раздел (:counter name="level 2" parent="" separator=":":)
Раздел (:counter name="level 3" parent="level 2" separator="-":)
Раздел (:counter name="level 3" parent="level 2" separator="-":)
Раздел (:counter name="level 3" parent="level 2" separator="-":)
Раздел (:counter name="level 2" parent="" separator=":":)
Раздел (:counter name="level 2" parent="" separator="-":)'''

        validResult = '''Раздел 1
Раздел 1:1
Раздел 1:1-1
Раздел 1:1-2
Раздел 1:1-3
Раздел 1:2
Раздел 1-3'''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

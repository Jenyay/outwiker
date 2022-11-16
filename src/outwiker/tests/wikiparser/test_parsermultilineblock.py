# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir
import outwiker.core.cssclasses as css


class ParserMultilineBlockTest(unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"
        self.filesPath = "testdata/samplefiles/"

        self.__createWiki()
        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def testMultilineBlockEmpty(self):
        text = "[{}]"
        result = ""

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockSimple_01(self):
        text = "Блаблабла [{Блок}] блабла"
        result = "Блаблабла Блок блабла"

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockSimple_02(self):
        text = "[{\\t}]"
        result = "\\t"

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockFormat_01(self):
        text = "Блаблабла [{Цитата '''полужирный шрифт''' [[Ссылка -> http://jenyay.net]] }] блабла"
        result = f'Блаблабла Цитата <b>полужирный шрифт</b> <a class="{css.CSS_WIKI}" href="http://jenyay.net">Ссылка</a>  блабла'

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockFormat_02(self):
        text = "[{[[Ссылка -> http://jenyay.net]]}]"
        result = f'<a class="{css.CSS_WIKI}" href="http://jenyay.net">Ссылка</a>'

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockFormat_03(self):
        text = "[{'''test'''}]"
        result = '<b>test</b>'

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockMultiline1(self):
        text = """Блаблабла [{это длинная
мнотострочная
цитата}] блабла"""

        result = """Блаблабла это длинная
мнотострочная
цитата блабла"""

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testMultilineBlockMultiline2(self):
        text = """Блаблабла
[{
это длинная
мнотострочная
цитата
}]
блабла"""

        result = """Блаблабла

это длинная
мнотострочная
цитата

блабла"""

        self.assertEqual(self.parser.toHtml(text), result)

    def testLineEnd_01(self):
        text = "[{Проверка[[<<]]Проверка}]"
        result = "Проверка<br/>Проверка"

        self.assertEqual(self.parser.toHtml(text), result)

# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class ParserQuoteTest(unittest.TestCase):
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

    def testQuoteEmpty(self):
        text = "[><]"
        result = '<blockquote class="ow-quote"></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteSimple_01(self):
        text = "Блаблабла [>Цитата<] блабла"
        result = 'Блаблабла <blockquote class="ow-quote">Цитата</blockquote> блабла'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteSimple_02(self):
        text = "[>\\t<]"
        result = '<blockquote class="ow-quote">\\t</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteFormat_01(self):
        text = "Блаблабла [>Цитата '''полужирный шрифт''' [[Ссылка -> http://jenyay.net]] <] блабла"
        result = 'Блаблабла <blockquote class="ow-quote">Цитата <b>полужирный шрифт</b> <a href="http://jenyay.net">Ссылка</a> </blockquote> блабла'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteFormat_02(self):
        text = "[>[[Ссылка -> http://jenyay.net]]<]"
        result = '<blockquote class="ow-quote"><a href="http://jenyay.net">Ссылка</a></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteFormat_03(self):
        text = "[>'''test'''<]"
        result = '<blockquote class="ow-quote"><b>test</b></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteMultiline1(self):
        text = """Блаблабла [>это длинная
мнотострочная
цитата<] блабла"""

        result = """Блаблабла <blockquote class="ow-quote">это длинная
мнотострочная
цитата</blockquote> блабла"""

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testQuoteMultiline2(self):
        text = """Блаблабла
[>
это длинная
мнотострочная
цитата
<]
блабла"""

        result = """Блаблабла
<blockquote class="ow-quote">
это длинная
мнотострочная
цитата
</blockquote>
блабла"""

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testNested_01(self):
        text = "[>[>Абырвалг<]<]"
        result = '<blockquote class="ow-quote"><blockquote class="ow-quote">Абырвалг</blockquote></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_02(self):
        text = "[>[>[>Абырвалг<]<]<]"
        result = '<blockquote class="ow-quote"><blockquote class="ow-quote"><blockquote class="ow-quote">Абырвалг</blockquote></blockquote></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_03(self):
        text = "[>Проверка [>Абырвалг<] 1-2-3<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote">Абырвалг</blockquote> 1-2-3</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_04_url(self):
        text = "[>Проверка [>http://jenyay.net<] 1-2-3<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote"><a href="http://jenyay.net">http://jenyay.net</a></blockquote> 1-2-3</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_05_url(self):
        text = "[>Проверка [>[[http://jenyay.net | Ссылка]]<] 1-2-3<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote"><a href="http://jenyay.net">Ссылка</a></blockquote> 1-2-3</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_06_url(self):
        text = "[>Проверка [>http://jenyay.net/image.png<] 1-2-3<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote"><img class="ow-image" src="http://jenyay.net/image.png"/></blockquote> 1-2-3</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result)

    def testNested_07(self):
        text = "[>Проверка [>Абырвалг<] 1-2-3 [>Абырвалг2<] 111<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote">Абырвалг</blockquote> 1-2-3 <blockquote class="ow-quote">Абырвалг2</blockquote> 111</blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_08(self):
        text = "[>Проверка [>Абырвалг<] '''1-2-3''' [>Абырвалг<]<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote">Абырвалг</blockquote> <b>1-2-3</b> <blockquote class="ow-quote">Абырвалг</blockquote></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_09(self):
        text = "[>Проверка [>Абырвалг<] [[http://example.com]] [>Абырвалг<]<]"
        result = '<blockquote class="ow-quote">Проверка <blockquote class="ow-quote">Абырвалг</blockquote> <a href="http://example.com">http://example.com</a> <blockquote class="ow-quote">Абырвалг</blockquote></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testNested_10(self):
        text = "[>[>[>Проверка<]<]<]"
        result = '<blockquote class="ow-quote"><blockquote class="ow-quote"><blockquote class="ow-quote">Проверка</blockquote></blockquote></blockquote>'

        self.assertEqual(self.parser.toHtml(text),
                         result,
                         self.parser.toHtml(text).encode(self.encoding))

    def testLineEnd_01(self):
        text = "[>Проверка[[<<]]Проверка<]"
        result = '<blockquote class="ow-quote">Проверка<br/>Проверка</blockquote>'

        self.assertEqual(self.parser.toHtml(text), result)

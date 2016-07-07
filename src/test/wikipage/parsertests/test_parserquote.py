# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserQuoteTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"
        self.filesPath = u"../test/samplefiles/"

        self.__createWiki()
        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def tearDown (self):
        removeDir (self.path)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def testQuoteEmpty (self):
        text = u"[><]"
        result = u"<blockquote></blockquote>"

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testQuoteSimple (self):
        text = u"Блаблабла [>Цитата<] блабла"
        result = u"Блаблабла <blockquote>Цитата</blockquote> блабла"

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testQuoteFormat (self):
        text = u"Блаблабла [>Цитата '''полужирный шрифт''' [[Ссылка -> http://jenyay.net]] <] блабла"
        result = u'Блаблабла <blockquote>Цитата <b>полужирный шрифт</b> <a href="http://jenyay.net">Ссылка</a> </blockquote> блабла'

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testQuoteMultiline1 (self):
        text = u"""Блаблабла [>это длинная
мнотострочная
цитата<] блабла"""

        result = u"""Блаблабла <blockquote>это длинная
мнотострочная
цитата</blockquote> блабла"""

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testQuoteMultiline2 (self):
        text = u"""Блаблабла
[>
это длинная
мнотострочная
цитата
<]
блабла"""

        result = u"""Блаблабла
<blockquote>
это длинная
мнотострочная
цитата
</blockquote>
блабла"""

        self.assertEqual (self.parser.toHtml (text),
                          result)


    def testNested_01 (self):
        text = u"[>[>Абырвалг<]<]"
        result = u"<blockquote><blockquote>Абырвалг</blockquote></blockquote>"

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testNested_02 (self):
        text = u"[>[>[>Абырвалг<]<]<]"
        result = u"<blockquote><blockquote><blockquote>Абырвалг</blockquote></blockquote></blockquote>"

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testNested_03 (self):
        text = u"[>Проверка [>Абырвалг<] 1-2-3<]"
        result = u"<blockquote>Проверка <blockquote>Абырвалг</blockquote> 1-2-3</blockquote>"

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testNested_04_url (self):
        text = u"[>Проверка [>http://jenyay.net<] 1-2-3<]"
        result = u'<blockquote>Проверка <blockquote><a href="http://jenyay.net">http://jenyay.net</a></blockquote> 1-2-3</blockquote>'

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testNested_05_url (self):
        text = u"[>Проверка [>[[http://jenyay.net | Ссылка]]<] 1-2-3<]"
        result = u'<blockquote>Проверка <blockquote><a href="http://jenyay.net">Ссылка</a></blockquote> 1-2-3</blockquote>'

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding))


    def testNested_06_url (self):
        text = u"[>Проверка [>http://jenyay.net/image.png<] 1-2-3<]"
        result = u'<blockquote>Проверка <blockquote><img src="http://jenyay.net/image.png"/></blockquote> 1-2-3</blockquote>'

        self.assertEqual (self.parser.toHtml (text),
                          result)

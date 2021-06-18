# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class ParserFormatTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.filesPath = "testdata/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)

    def __createWiki(self):
        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def test_monospaced_01(self):
        text = "бла-бла-бла @@моноширинный текст@@ бла-бла-бла"
        result = "бла-бла-бла <code>моноширинный текст</code> бла-бла-бла"

        self.assertEqual(self.parser.toHtml(text), result)

    def test_monospaced_02(self):
        text = "@@\\t@@"
        result = "<code>\\t</code>"

        self.assertEqual(self.parser.toHtml(text), result)

    def test_preformat_01(self):
        text = "[@ '''Полужирный''' \n''Курсив'' @]"
        result = "<pre> '''Полужирный''' \n''Курсив'' </pre>"

        self.assertEqual(self.parser.toHtml(text), result)

    def test_preformat_02(self):
        text = 'бла-бла-бла [@ <a href="http://jenyay.net/&param">jenyay.net</a> @] foo bar'
        result = 'бла-бла-бла <pre> &lt;a href="http://jenyay.net/&amp;param"&gt;jenyay.net&lt;/a&gt; </pre> foo bar'

        self.assertEqual(self.parser.toHtml(text), result)

    def test_preformat_03(self):
        text = "[@\\t@]"
        result = "<pre>\\t</pre>"

        self.assertEqual(self.parser.toHtml(text), result)

    def test_noformat_01(self):
        text = "[= '''Полужирный''' \n''Курсив'' =]"
        result = " '''Полужирный''' \n''Курсив'' "

        self.assertEqual(self.parser.toHtml(text), result)

    def test_noformat_02(self):
        text = "[=\\t=]"
        result = "\\t"

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_01(self):
        text = '<!-- Комментарий -->'
        result = ''

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_02(self):
        text = '[=<!-- Комментарий -->=]'
        result = '<!-- Комментарий -->'

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_03(self):
        text = '''<!-- Комментарий 
Бла-бла-бла
-->'''
        result = ''

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_04(self):
        text = '''Текст 1 <!-- Комментарий 
Бла-бла-бла
-->Текст 2'''
        result = 'Текст 1 Текст 2'

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_05(self):
        text = '* Текст<!-- Комментарий -->'
        result = '<ul><li>Текст</li></ul>'

        self.assertEqual(self.parser.toHtml(text), result)

    def test_comments_06(self):
        text = '!! Текст<!-- Комментарий -->'
        result = '<h1>Текст</h1>'

        self.assertEqual(self.parser.toHtml(text), result)

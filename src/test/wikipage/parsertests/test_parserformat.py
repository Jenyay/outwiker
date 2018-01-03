# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserFormatTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.filesPath = "../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)

    def __createWiki(self):
        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def testMonospaced_01(self):
        text = "бла-бла-бла @@моноширинный текст@@ бла-бла-бла"
        result = "бла-бла-бла <code>моноширинный текст</code> бла-бла-бла"

        self.assertEqual(self.parser.toHtml(text), result)

    def testMonospaced_02(self):
        text = "@@\\t@@"
        result = "<code>\\t</code>"

        self.assertEqual(self.parser.toHtml(text), result)

    def testPreformat1(self):
        text = "[@ '''Полужирный''' \n''Курсив'' @]"
        result = "<pre> '''Полужирный''' \n''Курсив'' </pre>"

        self.assertEqual(self.parser.toHtml(text), result)

    def testPreformat2(self):
        text = 'бла-бла-бла [@ <a href="http://jenyay.net/&param">jenyay.net</a> @] foo bar'
        result = 'бла-бла-бла <pre> &lt;a href="http://jenyay.net/&amp;param"&gt;jenyay.net&lt;/a&gt; </pre> foo bar'

        self.assertEqual(self.parser.toHtml(text), result)

    def testPreformat3(self):
        text = "[@\\t@]"
        result = "<pre>\\t</pre>"

        self.assertEqual(self.parser.toHtml(text), result)

    def testNoformat_01(self):
        text = "[= '''Полужирный''' \n''Курсив'' =]"
        result = " '''Полужирный''' \n''Курсив'' "

        self.assertEqual(self.parser.toHtml(text), result)

    def testNoformat_02(self):
        text = "[=\\t=]"
        result = "\\t"

        self.assertEqual(self.parser.toHtml(text), result)

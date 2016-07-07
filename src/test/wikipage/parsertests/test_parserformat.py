# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserFormatTest (unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def tearDown (self):
        removeDir (self.path)


    def __createWiki (self):
        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def testMonospaced (self):
        text = u"бла-бла-бла @@моноширинный текст@@ бла-бла-бла"
        result = u"бла-бла-бла <code>моноширинный текст</code> бла-бла-бла"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testPreformat1 (self):
        text = u"[@ '''Полужирный''' \n''Курсив'' @]"
        result = u"<pre> '''Полужирный''' \n''Курсив'' </pre>"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testPreformat2 (self):
        text = u'бла-бла-бла [@ <a href="http://jenyay.net/&param">jenyay.net</a> @] foo bar'
        result = u"бла-бла-бла <pre> &lt;a href=&quot;http://jenyay.net/&amp;param&quot;&gt;jenyay.net&lt;/a&gt; </pre> foo bar"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testNoformat (self):
        text = u"[= '''Полужирный''' \n''Курсив'' =]"
        result = u" '''Полужирный''' \n''Курсив'' "

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

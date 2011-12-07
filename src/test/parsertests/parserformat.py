#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserFormatTest (unittest.TestCase):
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
        

    def testMonospaced (self):
        text = u"бла-бла-бла @@моноширинный текст@@ бла-бла-бла"
        result = u"бла-бла-бла <CODE>моноширинный текст</CODE> бла-бла-бла"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testPreformat1 (self):
        text = u"[@ '''Полужирный''' \n''Курсив'' @]"
        result = u"<PRE> '''Полужирный''' \n''Курсив'' </PRE>"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testPreformat2 (self):
        text = u'бла-бла-бла [@ <a href="http://jenyay.net/&param">jenyay.net</a> @] foo bar'
        result = u"бла-бла-бла <PRE> &lt;a href=&quot;http://jenyay.net/&amp;param&quot;&gt;jenyay.net&lt;/a&gt; </PRE> foo bar"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testNoformat (self):
        text = u"[= '''Полужирный''' \n''Курсив'' =]"
        result = u" '''Полужирный''' \n''Курсив'' "

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

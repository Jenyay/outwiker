#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserAdHocTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.url1 = u"http://example.com"
        self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

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
        

    def tearDown(self):
        removeWiki (self.path)
    

    def testBoldSubscript (self):
        text = u"бла-бла-бла '''x'_c_'''' бла-бла-бла"
        result = u'бла-бла-бла <B>x<SUB>c</SUB></B> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testSubscriptBold (self):
        text = u"бла-бла-бла '_'''xc'''_' бла-бла-бла"
        result = u'бла-бла-бла <SUB><B>xc</B></SUB> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testBoldSuperscript (self):
        text = u"бла-бла-бла '''x'^c^'''' бла-бла-бла"
        result = u'бла-бла-бла <B>x<SUP>c</SUP></B> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testSuperscriptBold (self):
        text = u"бла-бла-бла '^'''xc'''^' бла-бла-бла"
        result = u'бла-бла-бла <SUP><B>xc</B></SUP> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    
    
    def testItalicSubscript (self):
        text = u"бла-бла-бла ''x'_c_''' бла-бла-бла"
        result = u'бла-бла-бла <I>x<SUB>c</SUB></I> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testItalicSuperscript (self):
        text = u"бла-бла-бла ''x'^c^''' бла-бла-бла"
        result = u'бла-бла-бла <I>x<SUP>c</SUP></I> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testBoldItalicSubscript (self):
        text = u"бла-бла-бла ''''x'_c_''''' бла-бла-бла"
        result = u'бла-бла-бла <B><I>x<SUB>c</SUB></I></B> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testBoldItalicSuperscript (self):
        text = u"бла-бла-бла ''''x'^c^''''' бла-бла-бла"
        result = u'бла-бла-бла <B><I>x<SUP>c</SUP></I></B> бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))



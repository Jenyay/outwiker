#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class ThumbListPluginTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/thumblist"]

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
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)


    def testContentParseEmpty (self):
        text = u"""Бла-бла-бла (:thumblist:) бла-бла-бла"""

        validResult = u"""Бла-бла-бла  бла-бла-бла"""

        result = self.parser.toHtml (text)
        self.assertEqual (validResult, result)


    def testAttach1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (os.path.exists (os.path.join (self.testPage.path, "__attach", "__thumb") ) )


    def testAttach2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u"image_01.JPG" in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)

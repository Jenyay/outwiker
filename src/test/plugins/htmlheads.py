#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeWiki


class HtmlHeadsTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/htmlheads"]

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
        self.assertEqual (len (self.loader), 1)

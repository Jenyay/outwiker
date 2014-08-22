# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeWiki


class TableOfContentsTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        self.__createWiki()

        self.pluginname = u"TableOfContents"
        dirlist = [u"../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        removeWiki (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testParser_01 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u""

        contents = parser.parse (text)

        self.assertEqual (contents, [])


    def testParser_02 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''  !! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (contents, [])

    def testParser_03 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u"Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")


    def testParser_04 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!!    Абырвалг    '''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u"Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

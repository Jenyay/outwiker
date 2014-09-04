# -*- coding: UTF-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class DiagrammerLoadingTest (BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp (self)
        self.wikipath = u"../test/testwiki"
        self.__createWiki (self.wikipath)

        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def __createWiki (self, wikipath):
        # Здесь будет создаваться вики
        removeWiki (wikipath)

        self.rootwiki = WikiDocument.create (wikipath)
        WikiPageFactory().create (self.rootwiki, u"Викистраница", [])
        TextPageFactory().create (self.rootwiki, u"Текст", [])


    def tearDown(self):
        Application.selectedPage = None
        Application.wikiroot = None
        removeWiki (self.wikipath)
        self.loader.clear()
        BaseMainWndTest.tearDown (self)


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
        self.assertNotEqual (self.loader["Diagrammer"], None)


    def testDestroy_01 (self):
        Application.wikiroot = None
        self.loader.clear()


    def testDestroy_02 (self):
        Application.wikiroot = self.rootwiki
        Application.selectedPage = None
        self.loader.clear()


    def testDestroy_03 (self):
        Application.wikiroot = self.rootwiki
        Application.selectedPage = self.rootwiki[u"Викистраница"]
        self.loader.clear()


    def testDestroy_04 (self):
        Application.wikiroot = self.rootwiki
        Application.selectedPage = self.rootwiki[u"Текст"]
        self.loader.clear()

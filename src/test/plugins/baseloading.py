# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class BasePluginLoadingTest (BaseMainWndTest):
    __metaclass__ = ABCMeta


    @abstractmethod
    def getPluginDir (self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        pass


    @abstractmethod
    def getPluginName (self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        pass


    def setUp(self):
        BaseMainWndTest.setUp (self)
        self.wikipath = u"../test/testwiki"
        self.__createWiki (self.wikipath)

        dirlist = [self.getPluginDir()]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def __createWiki (self, wikipath):
        # Здесь будет создаваться вики
        removeWiki (wikipath)

        self.rootwiki = WikiDocument.create (wikipath)
        WikiPageFactory().create (self.rootwiki, u"Викистраница", [])
        TextPageFactory().create (self.rootwiki, u"Текст", [])
        HtmlPageFactory().create (self.rootwiki, u"HTML", [])
        SearchPageFactory().create (self.rootwiki, u"Search", [])


    def tearDown(self):
        Application.selectedPage = None
        Application.wikiroot = None
        removeWiki (self.wikipath)
        self.loader.clear()
        BaseMainWndTest.tearDown (self)


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
        self.assertNotEqual (self.loader[self.getPluginName()], None)


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


    def testDestroy_05 (self):
        Application.wikiroot = self.rootwiki
        Application.selectedPage = self.rootwiki[u"HTML"]
        self.loader.clear()


    def testDestroy_06 (self):
        Application.wikiroot = self.rootwiki
        Application.selectedPage = self.rootwiki[u"Search"]
        self.loader.clear()

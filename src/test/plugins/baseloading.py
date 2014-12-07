# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.guitests.basemainwnd import BaseMainWndTest


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
        self.__createWiki ()

        dirlist = [self.getPluginDir()]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def __createWiki (self):
        # Здесь будет создаваться вики
        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        TextPageFactory().create (self.wikiroot, u"Текст", [])
        HtmlPageFactory().create (self.wikiroot, u"HTML", [])
        SearchPageFactory().create (self.wikiroot, u"Search", [])


    def tearDown(self):
        Application.selectedPage = None
        Application.wikiroot = None
        self.loader.clear()
        BaseMainWndTest.tearDown (self)


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
        self.assertNotEqual (self.loader[self.getPluginName()], None)


    def testDestroy_01 (self):
        Application.wikiroot = None
        self.loader.clear()


    def testDestroy_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        self.loader.clear()


    def testDestroy_03 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.loader.clear()


    def testDestroy_04 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Текст"]
        self.loader.clear()


    def testDestroy_05 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"HTML"]
        self.loader.clear()


    def testDestroy_06 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Search"]
        self.loader.clear()

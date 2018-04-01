# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class BasePluginLoadingTest(unittest.TestCase, BaseOutWikerGUIMixin,
                            metaclass=ABCMeta):
    @abstractmethod
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        pass

    @abstractmethod
    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        pass

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.__createWiki()

        dirlist = [self.getPluginDir()]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def __createWiki(self):
        # Здесь будет создаваться вики
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        TextPageFactory().create(self.wikiroot, "Текст", [])
        HtmlPageFactory().create(self.wikiroot, "HTML", [])
        SearchPageFactory().create(self.wikiroot, "Search", [])

    def tearDown(self):
        self.application.selectedPage = None
        self.application.wikiroot = None
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
        self.assertNotEqual(self.loader[self.getPluginName()], None)

    def testDestroy_01(self):
        self.application.wikiroot = None
        self.loader.clear()

    def testDestroy_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.loader.clear()

    def testDestroy_03(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.loader.clear()

    def testDestroy_04(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Текст"]
        self.loader.clear()

    def testDestroy_05(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML"]
        self.loader.clear()

    def testDestroy_06(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Search"]
        self.loader.clear()

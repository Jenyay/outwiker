# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.factoryselector import FactorySelector
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class TestPageTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """Тесты плагина TestPage"""

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.dirlist = ["../test/plugins/testpage"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(self.dirlist)

    def tearDown(self):
        self.application.wikiroot = None
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testAddRemoveFactory(self):
        plugin = self.loader["TestPage"]

        path = "../test/samplewiki"
        wikiroot = WikiDocument.load(path)

        test_page = wikiroot["Типы страниц/TestPage"]
        self.assertEqual(type(test_page), plugin.TestPage)

        self.assertEqual(type(FactorySelector.getFactory(plugin.TestPage.getTypeString())),
                         plugin.TestPageFactory)

        self.loader.clear()
        self.assertEqual(type(FactorySelector.getFactory(plugin.TestPage.getTypeString())),
                         TextPageFactory)

        self.loader.load(self.dirlist)

        self.assertEqual(type(FactorySelector.getFactory(plugin.TestPage.getTypeString())),
                         plugin.TestPageFactory)

    def testPageView(self):
        plugin = self.loader["TestPage"]

        wikiroot = WikiDocument.create(self.wikiroot.path)
        test_page = plugin.TestPageFactory().create(wikiroot, "Страница 1", [])

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        self.assertEqual(type(pageview), plugin.TestPageView)

    def testLoadContent(self):
        plugin = self.loader["TestPage"]

        wikiroot = WikiDocument.create(self.wikiroot.path)
        test_page = plugin.TestPageFactory().create(wikiroot, "Страница 1", [])

        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.text.GetValue()

        self.assertEqual(pageContent, "Абырвалг")

    def testChangeContent(self):
        plugin = self.loader["TestPage"]

        wikiroot = WikiDocument.create(self.wikiroot.path)
        test_page = plugin.TestPageFactory().create(wikiroot, "Страница 1", [])
        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageview.text.SetValue("Бла-бла-бла")

        self.application.selectedPage = None
        self.application.wikiroot = None

        wikiroot_other = WikiDocument.load(self.wikiroot.path)
        self.application.wikiroot = wikiroot_other
        self.application.selectedPage = wikiroot_other["Страница 1"]

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.text.GetValue()

        self.assertEqual(pageContent, "Бла-бла-бла")

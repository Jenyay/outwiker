# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.factoryselector import FactorySelector
from outwiker.gui.unknownpagetype import UnknownPageTypeFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin
from outwiker.tests.utils import removeDir


class WebPageTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """WebPage plugin tests"""

    def setUp(self):
        self.initApplication(createTreePanel=True)

        self.dirlist = ["plugins/webpage"]
        self.path = mkdtemp(
            prefix='OutWiker_Абырвалг абырвалг_' + str(self.__class__.__name__))

        self.loader = PluginsLoader(self.application)
        self.loader.load(self.dirlist)

    def tearDown(self):
        self.application.selectedPage = None
        self.application.wikiroot = None
        self.loader.clear()
        self.destroyApplication()
        if os.path.exists(self.path):
            removeDir(self.path)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testCreate(self):
        from webpage.webnotepage import WebPageFactory

        factory = WebPageFactory()
        wikiroot = createNotesTree(self.path)
        test_page = factory.create(wikiroot, "Страница 1", [])
        self.assertEqual(test_page.getTypeString(), factory.getPageTypeString())

        self.assertEqual(
            type(FactorySelector.getFactory(test_page.getTypeString())),
            WebPageFactory)

        self.loader.clear()
        self.assertEqual(type(FactorySelector.getFactory(test_page.getTypeString())),
                         UnknownPageTypeFactory)

        self.loader.load(self.dirlist)

        self.assertEqual(type(FactorySelector.getFactory(test_page.getTypeString())),
                         WebPageFactory)

    def testClear_01(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = createNotesTree(self.path)
        self.application.wikiroot = wikiroot

        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        self.application.selectedPage = test_page

        self.loader.clear()

    def testClear_02(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = createNotesTree(self.path)
        self.application.wikiroot = wikiroot

        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        self.application.selectedPage = test_page
        self.application.selectedPage = None

        self.loader.clear()

    def testPageView(self):
        from webpage.webnotepage import WebPageFactory
        from webpage.gui.webpageview import WebPageView

        wikiroot = createNotesTree(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        self.assertEqual(type(pageview), WebPageView)

    def testLoadContent(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = createNotesTree(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])

        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.codeEditor.GetText()

        self.assertEqual(pageContent, "Абырвалг")

    def testChangeContent(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = createNotesTree(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageview.codeEditor.SetText("Бла-бла-бла")
        pageview.Save()

        self.application.selectedPage = None
        self.application.wikiroot = None

        wikiroot_other = loadNotesTree(self.path)
        self.application.wikiroot = wikiroot_other
        self.application.selectedPage = wikiroot_other["Страница 1"]

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.codeEditor.GetText()

        self.assertEqual(pageContent, "Бла-бла-бла")

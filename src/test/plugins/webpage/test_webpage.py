# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.factoryselector import FactorySelector
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUIMixin
from test.utils import removeDir


class WebPageTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """WebPage plugin tests"""

    def setUp(self):
        self.initApplication()

        self.dirlist = ["../plugins/webpage"]
        self.path = mkdtemp(prefix='OutWiker_Абырвалг абырвалг_' + str(self.__class__.__name__))

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
        from webpage.webnotepage import WebPageFactory, WebNotePage

        wikiroot = WikiDocument.create(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        self.assertEqual(type(test_page), WebNotePage)

        self.assertEqual(
            type(FactorySelector.getFactory(WebNotePage.getTypeString())),
            WebPageFactory)

        self.loader.clear()
        self.assertEqual(type(FactorySelector.getFactory(WebNotePage.getTypeString())),
                         TextPageFactory)

        self.loader.load(self.dirlist)

        self.assertEqual(type(FactorySelector.getFactory(WebNotePage.getTypeString())),
                         WebPageFactory)

    def testClear_01(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create(self.path)
        self.application.wikiroot = wikiroot

        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        self.application.selectedPage = test_page

        self.loader.clear()

    def testClear_02(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create(self.path)
        self.application.wikiroot = wikiroot

        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        self.application.selectedPage = test_page
        self.application.selectedPage = None

        self.loader.clear()

    def testPageView(self):
        from webpage.webnotepage import WebPageFactory
        from webpage.gui.webpageview import WebPageView

        wikiroot = WikiDocument.create(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        self.assertEqual(type(pageview), WebPageView)

    def testLoadContent(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])

        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.codeEditor.GetText()

        self.assertEqual(pageContent, "Абырвалг")

    def testChangeContent(self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create(self.path)
        test_page = WebPageFactory().create(wikiroot, "Страница 1", [])
        test_page.content = "Абырвалг"

        self.application.wikiroot = wikiroot
        self.application.selectedPage = test_page

        pageview = self.application.mainWindow.pagePanel.pageView
        pageview.codeEditor.SetText("Бла-бла-бла")
        pageview.Save()

        self.application.selectedPage = None
        self.application.wikiroot = None

        wikiroot_other = WikiDocument.load(self.path)
        self.application.wikiroot = wikiroot_other
        self.application.selectedPage = wikiroot_other["Страница 1"]

        pageview = self.application.mainWindow.pagePanel.pageView
        pageContent = pageview.codeEditor.GetText()

        self.assertEqual(pageContent, "Бла-бла-бла")

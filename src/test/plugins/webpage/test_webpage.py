# -*- coding: UTF-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.factoryselector import FactorySelector
from outwiker.pages.text.textpage import TextPageFactory

from test.guitests.basemainwnd import BaseMainWndTest


class WebPageTest (BaseMainWndTest):
    """WebPage plugin tests"""

    def setUp (self):
        super (WebPageTest, self).setUp ()

        self.dirlist = [u"../plugins/webpage"]

        self.loader = PluginsLoader(Application)
        self.loader.load (self.dirlist)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testCreate (self):
        from webpage.webnotepage import WebPageFactory, WebNotePage

        wikiroot = WikiDocument.create (self.path)
        test_page = WebPageFactory().create (wikiroot, u"Страница 1", [])
        self.assertEqual (type (test_page), WebNotePage)

        self.assertEqual (
            type (FactorySelector.getFactory (WebNotePage.getTypeString())),
            WebPageFactory)

        self.loader.clear()
        self.assertEqual (type (FactorySelector.getFactory (WebNotePage.getTypeString())),
                          TextPageFactory)

        self.loader.load (self.dirlist)

        self.assertEqual (type (FactorySelector.getFactory (WebNotePage.getTypeString())),
                          WebPageFactory)


    def testClear_01 (self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create (self.path)
        Application.wikiroot = wikiroot

        test_page = WebPageFactory().create (wikiroot, u"Страница 1", [])
        Application.selectedPage = test_page

        self.loader.clear()


    def testClear_02 (self):
        from webpage.webnotepage import WebPageFactory

        wikiroot = WikiDocument.create (self.path)
        Application.wikiroot = wikiroot

        test_page = WebPageFactory().create (wikiroot, u"Страница 1", [])
        Application.selectedPage = test_page
        Application.selectedPage = None

        self.loader.clear()


    # def testPageView (self):
    #     plugin = self.loader[u"TestPage"]
    #
    #     wikiroot = WikiDocument.create (self.path)
    #     test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])
    #
    #     Application.wikiroot = wikiroot
    #     Application.selectedPage = test_page
    #
    #     pageview = Application.mainWindow.pagePanel.pageView
    #     self.assertEqual (type (pageview), plugin.TestPageView)
    #
    #
    # def testLoadContent (self):
    #     plugin = self.loader[u"TestPage"]
    #
    #     wikiroot = WikiDocument.create (self.path)
    #     test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])
    #
    #     test_page.content = u"Абырвалг"
    #
    #     Application.wikiroot = wikiroot
    #     Application.selectedPage = test_page
    #
    #     pageview = Application.mainWindow.pagePanel.pageView
    #     pageContent = pageview.text.GetValue()
    #
    #     self.assertEqual (pageContent, u"Абырвалг")
    #
    #
    # def testChangeContent (self):
    #     plugin = self.loader[u"TestPage"]
    #
    #     wikiroot = WikiDocument.create (self.path)
    #     test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])
    #     test_page.content = u"Абырвалг"
    #
    #     Application.wikiroot = wikiroot
    #     Application.selectedPage = test_page
    #
    #     pageview = Application.mainWindow.pagePanel.pageView
    #     pageview.text.SetValue (u"Бла-бла-бла")
    #
    #     Application.selectedPage = None
    #     Application.wikiroot = None
    #
    #     wikiroot_other = WikiDocument.load (self.path)
    #     Application.wikiroot = wikiroot_other
    #     Application.selectedPage = wikiroot_other[u"Страница 1"]
    #
    #     pageview = Application.mainWindow.pagePanel.pageView
    #     pageContent = pageview.text.GetValue()
    #
    #     self.assertEqual (pageContent, u"Бла-бла-бла")

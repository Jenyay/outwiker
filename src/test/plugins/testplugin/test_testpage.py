# -*- coding: UTF-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.factoryselector import FactorySelector
from outwiker.pages.text.textpage import TextPageFactory

from test.guitests.basemainwnd import BaseMainWndTest


class TestPageTest (BaseMainWndTest):
    """Тесты плагина TestPage"""

    def setUp (self):
        super (TestPageTest, self).setUp ()

        self.dirlist = [u"../test/plugins/testpage"]

        self.loader = PluginsLoader(Application)
        self.loader.load (self.dirlist)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testAddRemoveFactory (self):
        plugin = self.loader[u"TestPage"]

        path = u"../test/samplewiki"
        wikiroot = WikiDocument.load (path)

        test_page = wikiroot[u"Типы страниц/TestPage"]
        self.assertEqual (type (test_page), plugin.TestPage)

        self.assertEqual (type (FactorySelector.getFactory (plugin.TestPage.getTypeString())),
                          plugin.TestPageFactory)

        self.loader.clear()
        self.assertEqual (type (FactorySelector.getFactory (plugin.TestPage.getTypeString())),
                          TextPageFactory)

        self.loader.load (self.dirlist)

        self.assertEqual (type (FactorySelector.getFactory (plugin.TestPage.getTypeString())),
                          plugin.TestPageFactory)


    def testPageView (self):
        plugin = self.loader[u"TestPage"]

        wikiroot = WikiDocument.create (self.path)
        test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])

        Application.wikiroot = wikiroot
        Application.selectedPage = test_page

        pageview = Application.mainWindow.pagePanel.pageView
        self.assertEqual (type (pageview), plugin.TestPageView)


    def testLoadContent (self):
        plugin = self.loader[u"TestPage"]

        wikiroot = WikiDocument.create (self.path)
        test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])

        test_page.content = u"Абырвалг"

        Application.wikiroot = wikiroot
        Application.selectedPage = test_page

        pageview = Application.mainWindow.pagePanel.pageView
        pageContent = pageview.text.GetValue()

        self.assertEqual (pageContent, u"Абырвалг")


    def testChangeContent (self):
        plugin = self.loader[u"TestPage"]

        wikiroot = WikiDocument.create (self.path)
        test_page = plugin.TestPageFactory().create (wikiroot, u"Страница 1", [])
        test_page.content = u"Абырвалг"

        Application.wikiroot = wikiroot
        Application.selectedPage = test_page

        pageview = Application.mainWindow.pagePanel.pageView
        pageview.text.SetValue (u"Бла-бла-бла")

        Application.selectedPage = None
        Application.wikiroot = None

        wikiroot_other = WikiDocument.load (self.path)
        Application.wikiroot = wikiroot_other
        Application.selectedPage = wikiroot_other[u"Страница 1"]

        pageview = Application.mainWindow.pagePanel.pageView
        pageContent = pageview.text.GetValue()

        self.assertEqual (pageContent, u"Бла-бла-бла")

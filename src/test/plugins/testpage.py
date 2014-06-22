# -*- coding: UTF-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.factoryselector import FactorySelector
from outwiker.pages.text.textpage import TextPageFactory

from test.utils import removeWiki
from test.guitests.basemainwnd import BaseMainWndTest


class TestPageTest (BaseMainWndTest):
    """Тесты плагина TestPage"""
    def setUp (self):
        super (TestPageTest, self).setUp ()

        self.path = u"../test/testwiki"
        self.dirlist = [u"../plugins/testpage"]

        self.loader = PluginsLoader(Application)
        self.loader.load (self.dirlist)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)
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

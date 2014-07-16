# -*- coding: UTF-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class SessionsTest (BaseMainWndTest):
    """Тесты плагина Sessions"""
    def setUp (self):
        super (SessionsTest, self).setUp ()
        self.__createWiki()

        dirlist = [u"../plugins/sessions"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        super (SessionsTest, self).tearDown ()
        Application.wikiroot = None
        self.loader.clear()
        removeWiki (self.path)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory().create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory().create (self.rootwiki, u"Страница 2", [])
        WikiPageFactory().create (self.rootwiki[u"Страница 1"], u"Страница 3", [])
        WikiPageFactory().create (self.rootwiki[u"Страница 1/Страница 3"], u"Страница 4", [])


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)

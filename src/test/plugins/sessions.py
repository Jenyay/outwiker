# -*- coding: UTF-8 -*-

import os.path

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

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        WikiPageFactory().create (self.wikiroot[u"Страница 1"], u"Страница 3", [])
        WikiPageFactory().create (self.wikiroot[u"Страница 1/Страница 3"], u"Страница 4", [])


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testEmptySessions (self):
        storage = self.loader[u"Sessions"].SessionStorage(Application)

        self.assertEqual (storage.getSessions(), [])


    def testSaveSingleTab (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        storage = self.loader[u"Sessions"].SessionStorage(Application)
        storage.save (u"Имя сессии")

        sessionsList = storage.getSessions()

        self.assertEqual (len (sessionsList), 1)


    def testGetSessionInfo_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        storage = self.loader[u"Sessions"].SessionStorage(Application)

        session = storage.getSessionInfo()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 1)
        self.assertEqual (session.pages[0], self.wikiroot[u"Страница 1"])
        self.assertEqual (session.currentTab, 0)


    def testGetSessionInfo_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], False)

        storage = self.loader[u"Sessions"].SessionStorage(Application)

        session = storage.getSessionInfo()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 2)
        self.assertEqual (session.pages[0], self.wikiroot[u"Страница 1"])
        self.assertEqual (session.pages[1], self.wikiroot[u"Страница 2"])
        self.assertEqual (session.currentTab, 0)


    def testGetSessionInfo_03 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        storage = self.loader[u"Sessions"].SessionStorage(Application)

        session = storage.getSessionInfo()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 2)
        self.assertEqual (session.pages[0], self.wikiroot[u"Страница 1"])
        self.assertEqual (session.pages[1], self.wikiroot[u"Страница 2"])
        self.assertEqual (session.currentTab, 1)


    def testInvalidSession_01 (self):
        """
        Если нет открытых вики
        """
        Application.wikiroot = None
        storage = self.loader[u"Sessions"].SessionStorage(Application)

        session = storage.getSessionInfo()

        self.assertEqual (session.path, u"")
        self.assertEqual (len (session.pages), 0)
        self.assertEqual (session.currentTab, 0)

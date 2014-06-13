# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pageuiddepot import PageUidDepot

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeWiki


class PageUidDepotTest (unittest.TestCase):
    """Тест класса PageUidDepot"""
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        TextPageFactory.create (self.rootwiki, u"Страница 1", [])
        TextPageFactory.create (self.rootwiki, u"Страница 2", [])
        TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
        TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
        TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        Application.wikiroot = None


    def tearDown(self):
        Application.wikiroot = None
        removeWiki (self.path)


    def testEmpty (self):
        depot = PageUidDepot()
        self.assertEqual (depot[u"Абырвалг"], None)


    def testCreateUid_01 (self):
        depot = PageUidDepot()
        uid = depot.createUid (self.rootwiki[u"Страница 1"])
        self.assertEqual (depot[uid], self.rootwiki[u"Страница 1"])


    def testCreateUid_02 (self):
        depot = PageUidDepot()
        uid = depot.createUid (self.rootwiki[u"Страница 1"])
        uid_new = depot.createUid (self.rootwiki[u"Страница 1"])

        self.assertEqual (uid, uid_new)


    def testSaveLoad_01 (self):
        depot = PageUidDepot()
        uid = depot.createUid (self.rootwiki[u"Страница 1"])

        depot_new = PageUidDepot(self.rootwiki)

        self.assertEqual (depot_new[uid].title, u"Страница 1")


    def testSaveLoad_02 (self):
        depot = PageUidDepot()
        uid = depot.createUid (self.rootwiki[u"Страница 2/Страница 3/Страница 4"])

        depot_new = PageUidDepot(self.rootwiki)

        self.assertEqual (depot_new[uid].title, u"Страница 4")


    def testSaveLoad_03 (self):
        depot = PageUidDepot()
        uid = depot.createUid (self.rootwiki[u"Страница 1"])

        depot_new = PageUidDepot(self.rootwiki)

        self.assertEqual (depot_new[uid].title, u"Страница 1")

        removeWiki (self.path)


    def testRenamePage (self):
        depot = PageUidDepot()
        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = depot.createUid (page)

        page.title = u"Новый заголовок"
        self.assertEqual (depot[uid].title, u"Новый заголовок")

        depot_new = PageUidDepot(self.rootwiki)
        self.assertEqual (depot_new[uid].title, u"Новый заголовок")


    def testRemovePage (self):
        depot = PageUidDepot()
        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = depot.createUid (page)

        page.remove()
        self.assertEqual (depot[uid], None)


    def testMovePage (self):
        depot = PageUidDepot()
        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = depot.createUid (page)

        page.moveTo (self.rootwiki)
        self.assertEqual (depot[uid].title, u"Страница 3")

        depot_new = PageUidDepot(self.rootwiki)
        self.assertEqual (depot_new[uid].title, u"Страница 3")
        self.assertEqual (depot_new[uid].parent, self.rootwiki)


    def testApplication_01 (self):
        depot = PageUidDepot()
        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = depot.createUid (page)

        Application.wikiroot = self.rootwiki

        self.assertEqual (Application.pageUidDepot[uid].title, u"Страница 3")


    def testApplication_02 (self):
        Application.wikiroot = self.rootwiki

        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = Application.pageUidDepot.createUid (page)

        Application.wikiroot = None
        Application.wikiroot = self.rootwiki

        self.assertEqual (Application.pageUidDepot[uid].title, u"Страница 3")


    def testApplicationRenamePage (self):
        Application.wikiroot = self.rootwiki

        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = Application.pageUidDepot.createUid (page)

        page.title = u"Новый заголовок"
        self.assertEqual (Application.pageUidDepot[uid].title, u"Новый заголовок")


    def testApplicationRemovePage (self):
        Application.wikiroot = self.rootwiki

        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = Application.pageUidDepot.createUid (page)

        page.remove()
        self.assertEqual (Application.pageUidDepot[uid], None)


    def testApplicationMovePage (self):
        Application.wikiroot = self.rootwiki

        page = self.rootwiki[u"Страница 2/Страница 3"]
        uid = Application.pageUidDepot.createUid (page)

        page.moveTo (self.rootwiki)
        self.assertEqual (Application.pageUidDepot[uid].title, u"Страница 3")
        self.assertEqual (Application.pageUidDepot[uid].parent, self.rootwiki)

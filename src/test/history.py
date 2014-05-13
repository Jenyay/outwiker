# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.history import History, HistoryEmptyException

from outwiker.core.application import Application
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeWiki


class HistoryTest (unittest.TestCase):
    def setUp (self):
        # Количество срабатываний особытий при обновлении страницы
        self.treeUpdateCount = 0
        self.treeUpdateSender = None

        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wiki = WikiDocument.create (self.path)

        TextPageFactory.create (self.wiki, u"Страница 1", [])
        TextPageFactory.create (self.wiki, u"Страница 2", [])
        TextPageFactory.create (self.wiki[u"Страница 2"], u"Страница 3", [])
        TextPageFactory.create (self.wiki[u"Страница 2/Страница 3"], u"Страница 4", [])
        TextPageFactory.create (self.wiki[u"Страница 1"], u"Страница 5", [])

        Application.wikiroot = None


    def tearDown(self):
        removeWiki (self.path)
        Application.wikiroot = None


    def testEmpty (self):
        history = History()

        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 0)

        self.assertRaises (HistoryEmptyException, history.back)
        self.assertRaises (HistoryEmptyException, history.forward)


    def testAdd_01 (self):
        history = History()
        history.goto (self.wiki[u"Страница 1"])

        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 0)

        history.goto (self.wiki[u"Страница 2"])

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 0)

        history.goto (self.wiki[u"Страница 2"])

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 0)


    def testAdd_02 (self):
        history = History()
        history.goto (self.wiki[u"Страница 1"])

        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 0)

        # Если пытаемся добавить ту же самую страницу, что уже была до этого, ничего не делаем
        history.goto (self.wiki[u"Страница 1"])
        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 0)


    def testBackForward_01 (self):
        history = History()
        history.goto (self.wiki[u"Страница 1"])
        history.goto (self.wiki[u"Страница 2"])

        oldpage = history.back()

        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 1)
        self.assertEqual (oldpage, self.wiki[u"Страница 1"])

        oldpage = history.forward()

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 0)
        self.assertEqual (oldpage, self.wiki[u"Страница 2"])


    def testBackForward_02 (self):
        history = History()
        history.goto (self.wiki[u"Страница 1"])
        history.goto (self.wiki[u"Страница 2"])
        history.goto (self.wiki[u"Страница 2/Страница 3"])
        history.goto (self.wiki[u"Страница 2/Страница 3/Страница 4"])

        self.assertEqual (history.backLength, 3)
        self.assertEqual (history.forwardLength, 0)

        page = history.back()

        self.assertEqual (history.backLength, 2)
        self.assertEqual (history.forwardLength, 1)
        self.assertEqual (page, self.wiki[u"Страница 2/Страница 3"])

        page = history.back()

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 2)
        self.assertEqual (page, self.wiki[u"Страница 2"])

        page = history.back()

        self.assertEqual (history.backLength, 0)
        self.assertEqual (history.forwardLength, 3)
        self.assertEqual (page, self.wiki[u"Страница 1"])


        page = history.forward()

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 2)
        self.assertEqual (page, self.wiki[u"Страница 2"])

        page = history.forward()

        self.assertEqual (history.backLength, 2)
        self.assertEqual (history.forwardLength, 1)
        self.assertEqual (page, self.wiki[u"Страница 2/Страница 3"])

        page = history.forward()

        self.assertEqual (history.backLength, 3)
        self.assertEqual (history.forwardLength, 0)
        self.assertEqual (page, self.wiki[u"Страница 2/Страница 3/Страница 4"])


    def testBackForward_03 (self):
        history = History()
        history.goto (self.wiki[u"Страница 1"])
        history.goto (self.wiki[u"Страница 2"])
        history.goto (self.wiki[u"Страница 2/Страница 3"])
        history.goto (self.wiki[u"Страница 2/Страница 3/Страница 4"])

        history.back()
        page = history.back()

        self.assertEqual (history.backLength, 1)
        self.assertEqual (history.forwardLength, 2)
        self.assertEqual (page, self.wiki[u"Страница 2"])

        history.goto (self.wiki[u"Страница 1/Страница 5"])

        self.assertEqual (history.backLength, 2)
        self.assertEqual (history.forwardLength, 0)

        page = history.back()
        self.assertEqual (page, self.wiki[u"Страница 2"])

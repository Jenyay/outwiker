# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.history import History, HistoryEmptyException
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class HistoryTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # Количество срабатываний событий при обновлении страницы
        self.treeUpdateCount = 0
        self.treeUpdateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wiki = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wiki, "Страница 1", [])
        factory.create(self.wiki, "Страница 2", [])
        factory.create(self.wiki["Страница 2"], "Страница 3", [])
        factory.create(self.wiki["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wiki["Страница 1"], "Страница 5", [])

        self._application.wikiroot = None

    def tearDown(self):
        removeDir(self.path)
        self._application.wikiroot = None

    def testEmpty(self):
        history = History()

        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 0)

        self.assertRaises(HistoryEmptyException, history.back)
        self.assertRaises(HistoryEmptyException, history.forward)

        self.assertEqual(history.currentPage, None)

    def testGoto_01(self):
        history = History()
        history.goto(self.wiki["Страница 1"])

        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 0)
        self.assertEqual(history.currentPage, self.wiki["Страница 1"])

        history.goto(self.wiki["Страница 2"])

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 0)
        self.assertEqual(history.currentPage, self.wiki["Страница 2"])

        history.goto(self.wiki["Страница 2"])

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 0)
        self.assertEqual(history.currentPage, self.wiki["Страница 2"])

    def testGoto_02(self):
        history = History()
        history.goto(self.wiki["Страница 1"])

        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 0)

        # Если пытаемся добавить ту же самую страницу,
        # что уже была до этого, ничего не делаем
        history.goto(self.wiki["Страница 1"])
        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 0)

    def testBackForward_01(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])

        oldpage = history.back()

        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 1)
        self.assertEqual(oldpage, self.wiki["Страница 1"])
        self.assertEqual(history.currentPage, self.wiki["Страница 1"])

        oldpage = history.forward()

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 0)
        self.assertEqual(oldpage, self.wiki["Страница 2"])
        self.assertEqual(history.currentPage, self.wiki["Страница 2"])

    def testBackForward_02(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(history.backLength, 3)
        self.assertEqual(history.forwardLength, 0)

        page = history.back()

        self.assertEqual(history.backLength, 2)
        self.assertEqual(history.forwardLength, 1)
        self.assertEqual(page, self.wiki["Страница 2/Страница 3"])
        self.assertEqual(history.currentPage,
                         self.wiki["Страница 2/Страница 3"])

        page = history.back()

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 2)
        self.assertEqual(page, self.wiki["Страница 2"])
        self.assertEqual(history.currentPage, self.wiki["Страница 2"])

        page = history.back()

        self.assertEqual(history.backLength, 0)
        self.assertEqual(history.forwardLength, 3)
        self.assertEqual(page, self.wiki["Страница 1"])
        self.assertEqual(history.currentPage, self.wiki["Страница 1"])

        page = history.forward()

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 2)
        self.assertEqual(page, self.wiki["Страница 2"])
        self.assertEqual(history.currentPage, self.wiki["Страница 2"])

        page = history.forward()

        self.assertEqual(history.backLength, 2)
        self.assertEqual(history.forwardLength, 1)
        self.assertEqual(page, self.wiki["Страница 2/Страница 3"])
        self.assertEqual(history.currentPage,
                         self.wiki["Страница 2/Страница 3"])

        page = history.forward()

        self.assertEqual(history.backLength, 3)
        self.assertEqual(history.forwardLength, 0)
        self.assertEqual(page, self.wiki["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(history.currentPage,
                         self.wiki["Страница 2/Страница 3/Страница 4"])

    def testBackForward_03(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        history.back()
        page = history.back()

        self.assertEqual(history.backLength, 1)
        self.assertEqual(history.forwardLength, 2)
        self.assertEqual(page, self.wiki["Страница 2"])

        history.goto(self.wiki["Страница 1/Страница 5"])

        self.assertEqual(history.backLength, 2)
        self.assertEqual(history.forwardLength, 0)

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 2"])

    def testBackForward_04(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(None)
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])
        history.goto(self.wiki["Страница 2/Страница 3"])

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 2/Страница 3/Страница 4"])

        page = history.back()
        self.assertEqual(page, None)

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 2"])

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 1"])

    def testRename_01(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3"].title = "Новый заголовок"

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 2/Новый заголовок"])

    def testRename_02(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3/Страница 4"].title = "Новый заголовок"

        history.goto(None)
        page = history.back()

        self.assertEqual(page,
                         self.wiki["Страница 2/Страница 3/Новый заголовок"])

    def testRemove_01(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3"].remove()
        page = history.back()

        self.assertEqual(page, None)

    def testRemove_02(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        history.back()
        self.wiki["Страница 2/Страница 3/Страница 4"].remove()

        page = history.forward()

        self.assertEqual(page, None)

    def testRemove_03(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3/Страница 4"].remove()

        history.back()
        page = history.forward()

        self.assertEqual(page, None)

    def testMove_01(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3"].moveTo(self.wiki["Страница 1"])

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 1/Страница 3"])

    def testMove_02(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2"].moveTo(self.wiki["Страница 1"])

        page = history.back()
        self.assertEqual(page, self.wiki["Страница 1/Страница 2/Страница 3"])

    def testMove_03(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        history.back()

        self.wiki["Страница 2/Страница 3/Страница 4"].moveTo(
            self.wiki["Страница 1"])

        page = history.forward()
        self.assertEqual(page, self.wiki["Страница 1/Страница 4"])

    def testMove_04(self):
        history = History()
        history.goto(self.wiki["Страница 1"])
        history.goto(self.wiki["Страница 2"])
        history.goto(self.wiki["Страница 2/Страница 3"])
        history.goto(self.wiki["Страница 2/Страница 3/Страница 4"])

        self.wiki["Страница 2/Страница 3/Страница 4"].moveTo(
            self.wiki["Страница 1"])

        history.back()
        page = history.forward()
        self.assertEqual(page, self.wiki["Страница 1/Страница 4"])

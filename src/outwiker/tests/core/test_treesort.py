# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class TreeSortTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # Количество срабатываний событий при обновлении страницы
        self.treeUpdateCount = 0
        self.treeUpdateSender = None
        self._application.wikiroot = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 8", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 5", [])
        factory.create(self.wikiroot, "Страница 4", [])
        factory.create(self.wikiroot, "Страница 6", [])
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 3", [])
        factory.create(self.wikiroot, "Страница 7", [])

        self.wikiroot["Страница 8"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 5"].order = 2
        self.wikiroot["Страница 4"].order = 3
        self.wikiroot["Страница 6"].order = 4
        self.wikiroot["Страница 1"].order = 5
        self.wikiroot["Страница 3"].order = 6
        self.wikiroot["Страница 7"].order = 7

    def tearDown(self):
        self._application.wikiroot = None
        removeDir(self.path)

    def testSortAlphabetical1(self):
        """
        Сортировка записей по алфавиту
        """
        self.wikiroot.sortChildrenAlphabetical()

        children = self.wikiroot.children

        self.assertEqual(children[0], self.wikiroot["Страница 1"])
        self.assertEqual(children[1], self.wikiroot["Страница 2"])
        self.assertEqual(children[2], self.wikiroot["Страница 3"])
        self.assertEqual(children[3], self.wikiroot["Страница 4"])
        self.assertEqual(children[4], self.wikiroot["Страница 5"])
        self.assertEqual(children[5], self.wikiroot["Страница 6"])
        self.assertEqual(children[6], self.wikiroot["Страница 7"])
        self.assertEqual(children[7], self.wikiroot["Страница 8"])

    def testSortAlphabetical2(self):
        """
        Сортировка записей по алфавиту
        """
        self.wikiroot.sortChildrenAlphabetical()

        self.assertEqual(0, self.wikiroot["Страница 1"].order)
        self.assertEqual(1, self.wikiroot["Страница 2"].order)
        self.assertEqual(2, self.wikiroot["Страница 3"].order)
        self.assertEqual(3, self.wikiroot["Страница 4"].order)
        self.assertEqual(4, self.wikiroot["Страница 5"].order)
        self.assertEqual(5, self.wikiroot["Страница 6"].order)
        self.assertEqual(6, self.wikiroot["Страница 7"].order)
        self.assertEqual(7, self.wikiroot["Страница 8"].order)

    def testSortAlphabeticalEvent(self):
        self._application.wikiroot = self.wikiroot
        self._application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot.sortChildrenAlphabetical()

        self._application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual(1, self.treeUpdateCount)
        self.assertEqual(self.wikiroot, self.treeUpdateSender)

    def testSortAlphabeticalNoEvent(self):
        """
        Не устанавливает свойство self._application.wikiroot, поэтому событие не
 должно срабатывать
        """
        self._application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot.sortChildrenAlphabetical()

        self._application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual(0, self.treeUpdateCount)
        self.assertEqual(None, self.treeUpdateSender)

    def onEndTreeUpdate(self, sender):
        self.treeUpdateCount += 1
        self.treeUpdateSender = sender

    def testSortChildrenEvent(self):
        """
        Сортировка заметок, находящихся на более глубоком уровне вложения
        """
        factory = TextPageFactory()
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 8", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 2", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 5", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 1", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 3", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 7", [])

        self.wikiroot["Страница 1/Вложенная страница 8"].order = 0
        self.wikiroot["Страница 1/Вложенная страница 2"].order = 1
        self.wikiroot["Страница 1/Вложенная страница 5"].order = 2
        self.wikiroot["Страница 1/Вложенная страница 4"].order = 3
        self.wikiroot["Страница 1/Вложенная страница 6"].order = 4
        self.wikiroot["Страница 1/Вложенная страница 1"].order = 5
        self.wikiroot["Страница 1/Вложенная страница 3"].order = 6
        self.wikiroot["Страница 1/Вложенная страница 7"].order = 7

        self._application.wikiroot = self.wikiroot
        self._application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot["Страница 1"].sortChildrenAlphabetical()

        self._application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual(1, self.treeUpdateCount)
        self.assertEqual(self.wikiroot, self.treeUpdateSender)

    def testSortChildrenNoEvent(self):
        """
        Сортировка заметок, находящихся на более глубоком уровне вложения
        """
        factory = TextPageFactory()
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 8", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 2", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 5", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 1", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 3", [])
        factory.create(self.wikiroot["Страница 1"], "Вложенная страница 7", [])

        self.wikiroot["Страница 1/Вложенная страница 8"].order = 0
        self.wikiroot["Страница 1/Вложенная страница 2"].order = 1
        self.wikiroot["Страница 1/Вложенная страница 5"].order = 2
        self.wikiroot["Страница 1/Вложенная страница 4"].order = 3
        self.wikiroot["Страница 1/Вложенная страница 6"].order = 4
        self.wikiroot["Страница 1/Вложенная страница 1"].order = 5
        self.wikiroot["Страница 1/Вложенная страница 3"].order = 6
        self.wikiroot["Страница 1/Вложенная страница 7"].order = 7

        self._application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot["Страница 1"].sortChildrenAlphabetical()

        self._application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual(0, self.treeUpdateCount)
        self.assertEqual(None, self.treeUpdateSender)

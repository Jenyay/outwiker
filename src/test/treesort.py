# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.application import Application
from test.utils import removeWiki
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory


class TreeSortTest(unittest.TestCase):
    def setUp(self):
        # Количество срабатываний особытий при обновлении страницы
        self.treeUpdateCount = 0
        self.treeUpdateSender = None
        Application.wikiroot = None

        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 8", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot, u"Страница 5", [])
        factory.create (self.wikiroot, u"Страница 4", [])
        factory.create (self.wikiroot, u"Страница 6", [])
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 3", [])
        factory.create (self.wikiroot, u"Страница 7", [])

        self.wikiroot[u"Страница 8"].order = 0
        self.wikiroot[u"Страница 2"].order = 1
        self.wikiroot[u"Страница 5"].order = 2
        self.wikiroot[u"Страница 4"].order = 3
        self.wikiroot[u"Страница 6"].order = 4
        self.wikiroot[u"Страница 1"].order = 5
        self.wikiroot[u"Страница 3"].order = 6
        self.wikiroot[u"Страница 7"].order = 7


    def tearDown (self):
        Application.wikiroot = None


    def testSortAlphabetical1(self):
        """
        Сортировка записей по алфавиту
        """
        self.wikiroot.sortChildrenAlphabetical ()

        children = self.wikiroot.children

        self.assertEqual (children[0], self.wikiroot[u"Страница 1"])
        self.assertEqual (children[1], self.wikiroot[u"Страница 2"])
        self.assertEqual (children[2], self.wikiroot[u"Страница 3"])
        self.assertEqual (children[3], self.wikiroot[u"Страница 4"])
        self.assertEqual (children[4], self.wikiroot[u"Страница 5"])
        self.assertEqual (children[5], self.wikiroot[u"Страница 6"])
        self.assertEqual (children[6], self.wikiroot[u"Страница 7"])
        self.assertEqual (children[7], self.wikiroot[u"Страница 8"])


    def testSortAlphabetical2(self):
        """
        Сортировка записей по алфавиту
        """
        self.wikiroot.sortChildrenAlphabetical ()

        self.assertEqual (0, self.wikiroot[u"Страница 1"].order)
        self.assertEqual (1, self.wikiroot[u"Страница 2"].order)
        self.assertEqual (2, self.wikiroot[u"Страница 3"].order)
        self.assertEqual (3, self.wikiroot[u"Страница 4"].order)
        self.assertEqual (4, self.wikiroot[u"Страница 5"].order)
        self.assertEqual (5, self.wikiroot[u"Страница 6"].order)
        self.assertEqual (6, self.wikiroot[u"Страница 7"].order)
        self.assertEqual (7, self.wikiroot[u"Страница 8"].order)


    def testSortAlphabeticalEvent (self):
        Application.wikiroot = self.wikiroot
        Application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot.sortChildrenAlphabetical ()

        Application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual (1, self.treeUpdateCount)
        self.assertEqual (self.wikiroot, self.treeUpdateSender)


    def testSortAlphabeticalNoEvent (self):
        """
        Не устанавливает свойство Application.wikiroot, поэтому событие не должно срабатывать
        """
        Application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot.sortChildrenAlphabetical ()

        Application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual (0, self.treeUpdateCount)
        self.assertEqual (None, self.treeUpdateSender)


    def onEndTreeUpdate (self, sender):
        self.treeUpdateCount += 1
        self.treeUpdateSender = sender


    def testSortChildrenEvent (self):
        """
        Сортировка заметок, находящихся на более глубоком уровне вложения
        """
        factory = TextPageFactory()
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 8", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 2", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 5", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 6", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 1", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 3", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 7", [])

        self.wikiroot[u"Страница 1/Вложенная страница 8"].order = 0
        self.wikiroot[u"Страница 1/Вложенная страница 2"].order = 1
        self.wikiroot[u"Страница 1/Вложенная страница 5"].order = 2
        self.wikiroot[u"Страница 1/Вложенная страница 4"].order = 3
        self.wikiroot[u"Страница 1/Вложенная страница 6"].order = 4
        self.wikiroot[u"Страница 1/Вложенная страница 1"].order = 5
        self.wikiroot[u"Страница 1/Вложенная страница 3"].order = 6
        self.wikiroot[u"Страница 1/Вложенная страница 7"].order = 7


        Application.wikiroot = self.wikiroot
        Application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot[u"Страница 1"].sortChildrenAlphabetical ()

        Application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual (1, self.treeUpdateCount)
        self.assertEqual (self.wikiroot, self.treeUpdateSender)


    def testSortChildrenNoEvent (self):
        """
        Сортировка заметок, находящихся на более глубоком уровне вложения
        """
        factory = TextPageFactory()
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 8", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 2", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 5", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 6", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 1", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 3", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Вложенная страница 7", [])

        self.wikiroot[u"Страница 1/Вложенная страница 8"].order = 0
        self.wikiroot[u"Страница 1/Вложенная страница 2"].order = 1
        self.wikiroot[u"Страница 1/Вложенная страница 5"].order = 2
        self.wikiroot[u"Страница 1/Вложенная страница 4"].order = 3
        self.wikiroot[u"Страница 1/Вложенная страница 6"].order = 4
        self.wikiroot[u"Страница 1/Вложенная страница 1"].order = 5
        self.wikiroot[u"Страница 1/Вложенная страница 3"].order = 6
        self.wikiroot[u"Страница 1/Вложенная страница 7"].order = 7

        Application.onEndTreeUpdate += self.onEndTreeUpdate

        self.wikiroot[u"Страница 1"].sortChildrenAlphabetical ()

        Application.onEndTreeUpdate -= self.onEndTreeUpdate

        self.assertEqual (0, self.treeUpdateCount)
        self.assertEqual (None, self.treeUpdateSender)

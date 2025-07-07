# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.core.events import BookmarksChangedParams
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.tests.utils import removeDir


class BookmarksTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.bookmarkCount = 0
        self.bookmarkSender = None
        self._application.wikiroot = None

    def tearDown(self):
        self._application.wikiroot = None
        removeDir(self.path)

    def onBookmark(self, params: BookmarksChangedParams):
        self.bookmarkCount += 1
        self.bookmarkSender = params.bookmarks

    def testAddToBookmarks(self):
        # По умолчанию закладок нет
        self.assertEqual(len(self.wikiroot.bookmarks), 0)

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.wikiroot.bookmarks), 1)
        self.assertEqual(self.wikiroot.bookmarks[0].title, "Страница 1")

        # Проверим, что закладки сохраняются в конфиг
        wiki = loadNotesTree(self.path)

        self.assertEqual(len(wiki.bookmarks), 1)
        self.assertEqual(wiki.bookmarks[0].title, "Страница 1")

    def testManyBookmarks(self):
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(len(self.wikiroot.bookmarks), 3)
        self.assertEqual(self.wikiroot.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.wikiroot.bookmarks[1].subpath, "Страница 2")
        self.assertEqual(self.wikiroot.bookmarks[2].subpath,
                         "Страница 2/Страница 3")

    def testRemoveBookmarks(self):
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.wikiroot.bookmarks.remove(self.wikiroot["Страница 2"])

        self.assertEqual(len(self.wikiroot.bookmarks), 2)
        self.assertEqual(self.wikiroot.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.wikiroot.bookmarks[1].subpath,
                         "Страница 2/Страница 3")

    def testBookmarkEvent(self):
        self._application.onBookmarksChanged += self.onBookmark
        self._application.wikiroot = self.wikiroot

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self.wikiroot.bookmarks)

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 2)
        self.assertEqual(self.bookmarkSender, self.wikiroot.bookmarks)

        self.wikiroot.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 3)
        self.assertEqual(self.bookmarkSender, self.wikiroot.bookmarks)

    def testBookmarkNoEvent(self):
        self._application.onBookmarksChanged += self.onBookmark

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self.wikiroot.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

    def testPageInBookmarks(self):
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(
            self.wikiroot.bookmarks.pageMarked(self.wikiroot["Страница 1"]),
            True)

        self.assertEqual(
            self.wikiroot.bookmarks.pageMarked(
                self.wikiroot["Страница 2/Страница 3"]),
            True)

        self.assertEqual(
            self.wikiroot.bookmarks.pageMarked(
                self.wikiroot["Страница 1/Страница 5"]),
            False)

    def testCloneBookmarks(self):
        """
        Тест на повторное добавление одной и той же страницы
        """
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.wikiroot.bookmarks), 1)
        self.assertEqual(self.wikiroot.bookmarks[0].title, "Страница 1")

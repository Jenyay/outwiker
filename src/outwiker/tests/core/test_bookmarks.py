# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.core.bookmarks import Bookmarks
from outwiker.core.events import BookmarksChangedParams
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.tests.utils import removeDir


class BookmarksTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.wikiroot = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.bookmarkCount = 0
        self.bookmarkSender = None
        self.bookmarks = Bookmarks()
        self.bookmarks.setWikiRoot(self.wikiroot)
        self._application.wikiroot = None

    def tearDown(self):
        self._application.bookmarks.clear()
        self._application.wikiroot = None
        removeDir(self.path)

    def onBookmark(self, params: BookmarksChangedParams):
        self.bookmarkCount += 1
        self.bookmarkSender = params.bookmarks

    def testAddToBookmarks(self):
        # По умолчанию закладок нет
        self.assertEqual(len(self.bookmarks), 0)

        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

        # Проверим, что закладки сохраняются в конфиг
        other_bootmarks = Bookmarks()
        other_bootmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(len(other_bootmarks), 1)
        self.assertEqual(other_bootmarks[0].title, "Страница 1")

    def testManyBookmarks(self):
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(len(self.bookmarks), 3)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2")
        self.assertEqual(self.bookmarks[2].subpath, "Страница 2/Страница 3")

    def testRemoveBookmarks(self):
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.bookmarks.remove(self.wikiroot["Страница 2"])

        self.assertEqual(len(self.bookmarks), 2)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2/Страница 3")

    def testBookmarkEvent(self):
        self._application.onBookmarksChanged += self.onBookmark
        self._application.wikiroot = self.wikiroot
        self._application.bookmarks.setWikiRoot(self.wikiroot)

        self._application.bookmarks.add(self.wikiroot["Страница 1"])
        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

        self._application.bookmarks.add(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 2)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

        self._application.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 3)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

    def testBookmarkNoEvent(self):
        self._application.bookmarks.setWikiRoot(self.wikiroot)
        self._application.onBookmarksChanged += self.onBookmark

        self._application.bookmarks.add(self.wikiroot["Страница 1"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self._application.bookmarks.add(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self._application.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

    def testPageInBookmarks(self):
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(self.bookmarks.pageMarked(self.wikiroot["Страница 1"]), True)

        self.assertEqual(
            self.bookmarks.pageMarked(self.wikiroot["Страница 2/Страница 3"]), True
        )

        self.assertEqual(
            self.bookmarks.pageMarked(self.wikiroot["Страница 1/Страница 5"]), False
        )

    def testCloneBookmarks(self):
        """
        Тест на повторное добавление одной и той же страницы
        """
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

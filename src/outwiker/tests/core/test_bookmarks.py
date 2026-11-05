# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.bookmarks import Bookmarks
from outwiker.core.config import StringListSection
from outwiker.core.events import BookmarksChangedParams
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.tests.utils import removeDir


class BookmarksTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # The wiki will be created here
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
        self.bookmarkPages = []
        self.bookmarkAction = 0
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
        self.bookmarkPages = params.pages
        self.bookmarkAction = params.action

    def testAddToBookmarks_AsSubpath(self):
        # No bookmarks by default
        self.assertEqual(len(self.bookmarks), 0)

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

        # Check that bookmarks are saved to the config
        other_bootmarks = Bookmarks()
        other_bootmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(len(other_bootmarks), 1)
        self.assertEqual(other_bootmarks[0].title, "Страница 1")

    def testAddToBookmarks_AsPageUID(self):
        # No bookmarks by default
        self.assertEqual(len(self.bookmarks), 0)

        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

        # Check that bookmarks are saved to the config
        other_bootmarks = Bookmarks()
        other_bootmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(len(other_bootmarks), 1)
        self.assertEqual(other_bootmarks[0].title, "Страница 1")

    def testManyBookmarks_AsPageUID(self):
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(len(self.bookmarks), 3)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2")
        self.assertEqual(self.bookmarks[2].subpath, "Страница 2/Страница 3")

    def testManyBookmarksAsSubpage(self):
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.assertEqual(len(self.bookmarks), 3)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2")
        self.assertEqual(self.bookmarks[2].subpath, "Страница 2/Страница 3")

    def testRemoveBookmarks_AsSubpath(self):
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.bookmarks.remove(self.wikiroot["Страница 2"])

        self.assertEqual(len(self.bookmarks), 2)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2/Страница 3")

    def testRemoveBookmarks_AsPageUID(self):
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.bookmarks.remove(self.wikiroot["Страница 2"])

        self.assertEqual(len(self.bookmarks), 2)
        self.assertEqual(self.bookmarks[0].subpath, "Страница 1")
        self.assertEqual(self.bookmarks[1].subpath, "Страница 2/Страница 3")

    def testBookmarkEvent_AsPageUID(self):
        self._application.onBookmarksChanged += self.onBookmark
        self._application.wikiroot = self.wikiroot
        self._application.bookmarks.setWikiRoot(self.wikiroot)

        self._application.bookmarks.add(self.wikiroot["Страница 1"])
        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)
        self.assertEqual(self.bookmarkPages, [self.wikiroot["Страница 1"]])

        self._application.bookmarks.add(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 2)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

        self._application.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 3)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

    def testBookmarkEvent_AsSubpath(self):
        self._application.onBookmarksChanged += self.onBookmark
        self._application.wikiroot = self.wikiroot
        self._application.bookmarks.setWikiRoot(self.wikiroot)

        self._application.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

        self._application.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.assertEqual(self.bookmarkCount, 2)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

        self._application.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 3)
        self.assertEqual(self.bookmarkSender, self._application.bookmarks)

    def testBookmarkNoEvent_AsPageUID(self):
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

    def testBookmarkNoEvent_AsSubpath(self):
        self._application.bookmarks.setWikiRoot(self.wikiroot)
        self._application.onBookmarksChanged += self.onBookmark

        self._application.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self._application.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

        self._application.bookmarks.remove(self.wikiroot["Страница 2"])
        self.assertEqual(self.bookmarkCount, 0)
        self.assertEqual(self.bookmarkSender, None)

    def testPageInBookmarks_AsPageUID(self):
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

    def testPageInBookmarks_AsSubpath(self):
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.assertEqual(self.bookmarks.pageMarked(self.wikiroot["Страница 1"]), True)

        self.assertEqual(
            self.bookmarks.pageMarked(self.wikiroot["Страница 2/Страница 3"]), True
        )

        self.assertEqual(
            self.bookmarks.pageMarked(self.wikiroot["Страница 1/Страница 5"]), False
        )

    def testCloneBookmarks_AsPageUID(self):
        """
        Test for re-adding the same page
        """
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

    def testCloneBookmarks_AsSubpath(self):
        """
        Test for re-adding the same page
        """
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)

        self.assertEqual(len(self.bookmarks), 1)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")

    def testSetBookmarks(self):
        # No bookmarks by default
        self.assertEqual(len(self.bookmarks), 0)

        pages = [self.wikiroot["Страница 1"], self.wikiroot["Страница 2"], self.wikiroot["Страница 2/Страница 3"]]
        self.bookmarks.setBookmarks(pages)

        self.assertEqual(len(self.bookmarks), 3)
        self.assertEqual(self.bookmarks[0].title, "Страница 1")
        self.assertEqual(self.bookmarks[1].title, "Страница 2")
        self.assertEqual(self.bookmarks[2].title, "Страница 3")

        # Check that bookmarks are saved to the config
        other_bookmarks = Bookmarks()
        other_bookmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(len(other_bookmarks), 3)
        self.assertEqual(other_bookmarks[0].title, "Страница 1")
        self.assertEqual(other_bookmarks[1].title, "Страница 2")
        self.assertEqual(other_bookmarks[2].title, "Страница 3")

    def testSetBookmarksEventContainsOldAndNewPages(self):
        """
        BookmarksChangedParams.pages must contain both pages that were
        bookmarked before setBookmarks() call and pages passed to it
        """
        # Old bookmarks
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.bookmarks.onBookmarksChanged += self.onBookmark

        # New pages: "Страница 1/Страница 5" is not bookmarked yet,
        # "Страница 1" is already bookmarked
        pages = [
            self.wikiroot["Страница 1/Страница 5"],
            self.wikiroot["Страница 1"],
        ]
        self.bookmarks.setBookmarks(pages)

        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self.bookmarks)
        self.assertEqual(self.bookmarkAction, BookmarksChangedParams.ACTION_FULL_UPDATE)

        expected_subpaths = {
            "Страница 1",
            "Страница 2/Страница 3",
            "Страница 1/Страница 5",
        }
        self.assertEqual(
            {page.subpath for page in self.bookmarkPages}, expected_subpaths
        )
        # "Страница 1" must be mentioned only once
        self.assertEqual(len(self.bookmarkPages), len(expected_subpaths))

    def testSetBookmarksEventContainsOldAndNewPages_AsSubpath(self):
        """
        Same as testSetBookmarksEventContainsOldAndNewPages, but old
        bookmarks are stored in config as subpaths
        """
        # Old bookmarks stored as subpaths
        self.bookmarks.add(self.wikiroot["Страница 2"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.bookmarks.onBookmarksChanged += self.onBookmark

        pages = [
            self.wikiroot["Страница 2/Страница 3/Страница 4"],
            self.wikiroot["Страница 2"],
        ]
        self.bookmarks.setBookmarks(pages)

        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self.bookmarks)
        self.assertEqual(self.bookmarkAction, BookmarksChangedParams.ACTION_FULL_UPDATE)

        expected_subpaths = {
            "Страница 2",
            "Страница 2/Страница 3",
            "Страница 2/Страница 3/Страница 4",
        }
        self.assertEqual(
            {page.subpath for page in self.bookmarkPages}, expected_subpaths
        )
        self.assertEqual(len(self.bookmarkPages), len(expected_subpaths))

    def testSetBookmarksEventNoOldBookmarks(self):
        """
        If there were no bookmarks before setBookmarks() call,
        BookmarksChangedParams.pages must contain only passed pages
        """
        self.assertEqual(len(self.bookmarks), 0)

        self.bookmarks.onBookmarksChanged += self.onBookmark

        pages = [
            self.wikiroot["Страница 1"],
            self.wikiroot["Страница 2"],
        ]
        self.bookmarks.setBookmarks(pages)

        self.assertEqual(self.bookmarkCount, 1)
        self.assertEqual(self.bookmarkSender, self.bookmarks)
        self.assertEqual(self.bookmarkAction, BookmarksChangedParams.ACTION_FULL_UPDATE)

        self.assertEqual(
            {page.subpath for page in self.bookmarkPages},
            {"Страница 1", "Страница 2"},
        )
        self.assertEqual(len(self.bookmarkPages), 2)

    def testSubpathBookmarks(self):
        config = StringListSection(
            self.wikiroot.params, Bookmarks.CONFIG_SECTION, Bookmarks.CONFIG_OPTION
        )
        config.value = [
            self.wikiroot["Страница 1"].subpath,
            self.wikiroot["Страница 2/Страница 3"].subpath,
        ]

        bookmarks = Bookmarks()
        bookmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(bookmarks[0].title, "Страница 1")
        self.assertEqual(bookmarks[1].title, "Страница 3")

    def testPageUIDBookmarks(self):
        config = StringListSection(
            self.wikiroot.params, Bookmarks.CONFIG_SECTION, Bookmarks.CONFIG_OPTION
        )
        config.value = [
            self.wikiroot["Страница 1"].getUid(generate=True),
            self.wikiroot["Страница 2/Страница 3"].getUid(generate=True),
        ]

        bookmarks = Bookmarks()
        bookmarks.setWikiRoot(self.wikiroot)

        self.assertEqual(bookmarks[0].title, "Страница 1")
        self.assertEqual(bookmarks[1].title, "Страница 3")

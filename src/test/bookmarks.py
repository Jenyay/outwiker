#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument

from outwiker.pages.text.textpage import TextPageFactory

from outwiker.core.application import Application
from test.utils import removeWiki


class BookmarksTest (unittest.TestCase):
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

        self.bookmarkCount = 0
        self.bookmarkSender = None
        Application.wikiroot = None


    def tearDown (self):
        Application.wikiroot = None
        removeWiki (self.path)


    def onBookmark (self, bookmarks):
        self.bookmarkCount += 1
        self.bookmarkSender = bookmarks
    

    def testAddToBookmarks (self):
        # По умолчанию закладок нет
        self.assertEqual (len (self.rootwiki.bookmarks), 0)

        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

        self.assertEqual (len (self.rootwiki.bookmarks), 1)
        self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")

        # Проверим, что закладки сохраняются в конфиг
        wiki = WikiDocument.load (self.path)

        self.assertEqual (len (wiki.bookmarks), 1)
        self.assertEqual (wiki.bookmarks[0].title, u"Страница 1")
    

    def testManyBookmarks (self):
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

        self.assertEqual (len (self.rootwiki.bookmarks), 3)
        self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
        self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2")
        self.assertEqual (self.rootwiki.bookmarks[2].subpath, u"Страница 2/Страница 3")
    

    def testRemoveBookmarks (self):
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

        self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])

        self.assertEqual (len (self.rootwiki.bookmarks), 2)
        self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
        self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2/Страница 3")
    

    def testBookmarkEvent (self):
        Application.onBookmarksChanged += self.onBookmark
        Application.wikiroot = self.rootwiki

        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.assertEqual (self.bookmarkCount, 1)
        self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)

        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 2)
        self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)


        self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 3)
        self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)


    def testBookmarkNoEvent (self):
        Application.onBookmarksChanged += self.onBookmark

        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)

        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)


        self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)
    

    def testPageInBookmarks (self):
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

        self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1"]), 
                True)

        self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 2/Страница 3"]),
                True)

        self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1/Страница 5"]), 
                False)
    

    def testCloneBookmarks (self):
        """
        Тест на повторное добавление одной и той же страницы
        """
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
        self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

        self.assertEqual (len (self.rootwiki.bookmarks), 1)
        self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")





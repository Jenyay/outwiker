# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from test.utils import removeDir


class BookmarksTest (unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        self.bookmarkCount = 0
        self.bookmarkSender = None
        Application.wikiroot = None


    def tearDown (self):
        Application.wikiroot = None
        removeDir (self.path)


    def onBookmark (self, bookmarks):
        self.bookmarkCount += 1
        self.bookmarkSender = bookmarks


    def testAddToBookmarks (self):
        # По умолчанию закладок нет
        self.assertEqual (len (self.wikiroot.bookmarks), 0)

        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])

        self.assertEqual (len (self.wikiroot.bookmarks), 1)
        self.assertEqual (self.wikiroot.bookmarks[0].title, u"Страница 1")

        # Проверим, что закладки сохраняются в конфиг
        wiki = WikiDocument.load (self.path)

        self.assertEqual (len (wiki.bookmarks), 1)
        self.assertEqual (wiki.bookmarks[0].title, u"Страница 1")


    def testManyBookmarks (self):
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2/Страница 3"])

        self.assertEqual (len (self.wikiroot.bookmarks), 3)
        self.assertEqual (self.wikiroot.bookmarks[0].subpath, u"Страница 1")
        self.assertEqual (self.wikiroot.bookmarks[1].subpath, u"Страница 2")
        self.assertEqual (self.wikiroot.bookmarks[2].subpath, u"Страница 2/Страница 3")


    def testRemoveBookmarks (self):
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2/Страница 3"])

        self.wikiroot.bookmarks.remove (self.wikiroot[u"Страница 2"])

        self.assertEqual (len (self.wikiroot.bookmarks), 2)
        self.assertEqual (self.wikiroot.bookmarks[0].subpath, u"Страница 1")
        self.assertEqual (self.wikiroot.bookmarks[1].subpath, u"Страница 2/Страница 3")


    def testBookmarkEvent (self):
        Application.onBookmarksChanged += self.onBookmark
        Application.wikiroot = self.wikiroot

        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.assertEqual (self.bookmarkCount, 1)
        self.assertEqual (self.bookmarkSender, self.wikiroot.bookmarks)

        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 2)
        self.assertEqual (self.bookmarkSender, self.wikiroot.bookmarks)


        self.wikiroot.bookmarks.remove (self.wikiroot[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 3)
        self.assertEqual (self.bookmarkSender, self.wikiroot.bookmarks)


    def testBookmarkNoEvent (self):
        Application.onBookmarksChanged += self.onBookmark

        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)

        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)


        self.wikiroot.bookmarks.remove (self.wikiroot[u"Страница 2"])
        self.assertEqual (self.bookmarkCount, 0)
        self.assertEqual (self.bookmarkSender, None)


    def testPageInBookmarks (self):
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot.bookmarks.pageMarked (self.wikiroot[u"Страница 1"]),
                          True)

        self.assertEqual (self.wikiroot.bookmarks.pageMarked (self.wikiroot[u"Страница 2/Страница 3"]),
                          True)

        self.assertEqual (self.wikiroot.bookmarks.pageMarked (self.wikiroot[u"Страница 1/Страница 5"]),
                          False)


    def testCloneBookmarks (self):
        """
        Тест на повторное добавление одной и той же страницы
        """
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])
        self.wikiroot.bookmarks.add (self.wikiroot[u"Страница 1"])

        self.assertEqual (len (self.wikiroot.bookmarks), 1)
        self.assertEqual (self.wikiroot.bookmarks[0].title, u"Страница 1")

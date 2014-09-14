# -*- coding: UTF-8 -*-

import os.path
import unittest


from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.exceptions import DublicateTitle
from outwiker.core.tree import WikiDocument

from test.utils import removeWiki


class RenameTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])
        factory.create (self.wikiroot, u"Страница 6", [])

        self.treeUpdateCount = 0
        self.eventSender = None

        Application.wikiroot = None


    def __onPageRename (self, page, oldSubpath):
        self.treeUpdateCount += 1
        self.eventSender = page


    def tearDown (self):
        Application.wikiroot = None


    def testRename1 (self):
        page = self.wikiroot[u"Страница 1"]
        page.title = u"Страница 1 new"

        self.assertEqual (page.title, u"Страница 1 new")
        self.assertEqual (self.wikiroot[u"Страница 1 new"], page)
        self.assertEqual (page.subpath, u"Страница 1 new")
        self.assertEqual (self.wikiroot[u"Страница 1"], None)
        self.assertTrue (os.path.exists (self.wikiroot[u"Страница 1 new"].path))


    def testEvent (self):
        Application.onPageRename += self.__onPageRename
        Application.wikiroot = self.wikiroot

        page = self.wikiroot[u"Страница 1"]
        page.title = u"Страница 1 new"

        self.assertEqual (self.treeUpdateCount, 1)
        self.assertEqual (self.eventSender, self.wikiroot[u"Страница 1 new"])
        self.assertEqual (self.eventSender, page)

        Application.onPageRename -= self.__onPageRename


    def testNoEvent (self):
        Application.onPageRename += self.__onPageRename

        page = self.wikiroot[u"Страница 1"]
        page.title = u"Страница 1 new"

        self.assertEqual (self.treeUpdateCount, 0)
        self.assertEqual (self.eventSender, None)

        Application.onPageRename -= self.__onPageRename


    def testInvalidRename (self):
        def rename (page, newtitle):
            page.title = newtitle

        self.assertRaises (DublicateTitle, rename,
                           self.wikiroot[u"Страница 1"], u"СтраНица 6")


    def testRename2 (self):
        page = self.wikiroot[u"Страница 2/Страница 3"]
        page.title = u"Страница 3 new"

        self.assertEqual (page.title, u"Страница 3 new")
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3 new"], page)
        self.assertEqual (page.subpath, u"Страница 2/Страница 3 new")
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3"], None)


    def testRename3 (self):
        page3 = self.wikiroot[u"Страница 2/Страница 3"]
        page4 = page3[u"Страница 4"]

        page3.title = u"Страница 3 new"

        self.assertEqual (page3[u"Страница 4"], page4)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3 new/Страница 4"], page4)


    def testRename4 (self):
        page = self.wikiroot[u"Страница 1"]
        page.title = u"СтрАницА 1"

        self.assertEqual (page.title, u"СтрАницА 1")
        self.assertEqual (self.wikiroot[u"СтрАницА 1"], page)
        self.assertEqual (page.subpath, u"СтрАницА 1")


    def testLoad (self):
        page = self.wikiroot[u"Страница 1"]
        page.title = u"Страница 1 new"

        wiki = WikiDocument.load (self.path)
        self.assertNotEqual (wiki[u"Страница 1 new"], None)
        self.assertEqual (wiki[u"Страница 1"], None)


    def testBookmarks1 (self):
        page = self.wikiroot[u"Страница 6"]
        self.wikiroot.bookmarks.add (page)
        page.title = u"Страница 6 new"

        self.assertTrue (self.wikiroot.bookmarks.pageMarked (page))


    def testBookmarks2 (self):
        page2 = self.wikiroot[u"Страница 2"]
        page3 = self.wikiroot[u"Страница 2/Страница 3"]
        page4 = self.wikiroot[u"Страница 2/Страница 3/Страница 4"]

        self.wikiroot.bookmarks.add (page2)
        self.wikiroot.bookmarks.add (page3)
        self.wikiroot.bookmarks.add (page4)

        page2.title = u"Страница 2 new"

        self.assertTrue (self.wikiroot.bookmarks.pageMarked (page2))
        self.assertTrue (self.wikiroot.bookmarks.pageMarked (page3))
        self.assertTrue (self.wikiroot.bookmarks.pageMarked (page4))


    def testPath (self):
        page2 = self.wikiroot[u"Страница 2"]
        page3 = self.wikiroot[u"Страница 2/Страница 3"]
        page4 = self.wikiroot[u"Страница 2/Страница 3/Страница 4"]

        page2.title = u"Страница 2 new"

        self.assertEqual (page2.path, os.path.join (self.path, u"Страница 2 new"))
        self.assertEqual (page3.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3"))
        self.assertEqual (page4.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3", u"Страница 4"))


    def testConfig (self):
        page2 = self.wikiroot[u"Страница 2"]
        page3 = self.wikiroot[u"Страница 2/Страница 3"]
        page4 = self.wikiroot[u"Страница 2/Страница 3/Страница 4"]

        page2.title = u"Страница 2 new"

        page2.tags = [u"тег 1"]
        page3.tags = [u"тег 2"]
        page4.tags = [u"тег 3"]

        self.assertEqual (page2.tags[0], u"тег 1")
        self.assertEqual (page3.tags[0], u"тег 2")
        self.assertEqual (page4.tags[0], u"тег 3")


    def testRenameError (self):
        page = self.wikiroot[u"Страница 2"]
        attach = Attachment (page)

        with open (attach.getFullPath ("111.txt", True), "w"):
            try:
                page.title = u"Новое имя"
            except OSError:
                pass
            else:
                self.assertTrue (os.path.exists (self.wikiroot[u"Новое имя"].path))
                self.assertEqual (self.wikiroot[u"Страница 2"], None)

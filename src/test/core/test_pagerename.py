# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.exceptions import DuplicateTitle
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory

from test.utils import removeDir


class RenameTest(unittest.TestCase):
    def setUp(self):
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        factory.create(self.wikiroot, "Страница 6", [])

        self.treeUpdateCount = 0
        self.eventSender = None

        Application.wikiroot = None

    def __onPageRename(self, page, oldSubpath):
        self.treeUpdateCount += 1
        self.eventSender = page

    def tearDown(self):
        Application.wikiroot = None
        removeDir(self.path)

    def testRename1(self):
        page = self.wikiroot["Страница 1"]
        page.title = "Страница 1 new"

        self.assertEqual(page.title, "Страница 1 new")
        self.assertEqual(self.wikiroot["Страница 1 new"], page)
        self.assertEqual(page.subpath, "Страница 1 new")
        self.assertEqual(self.wikiroot["Страница 1"], None)
        self.assertTrue(os.path.exists(self.wikiroot["Страница 1 new"].path))

    def testEvent(self):
        Application.onPageRename += self.__onPageRename
        Application.wikiroot = self.wikiroot

        page = self.wikiroot["Страница 1"]
        page.title = "Страница 1 new"

        self.assertEqual(self.treeUpdateCount, 1)
        self.assertEqual(self.eventSender, self.wikiroot["Страница 1 new"])
        self.assertEqual(self.eventSender, page)
        Application.onPageRename -= self.__onPageRename

    def testNoEvent(self):
        Application.onPageRename += self.__onPageRename

        page = self.wikiroot["Страница 1"]
        page.title = "Страница 1 new"

        self.assertEqual(self.treeUpdateCount, 0)
        self.assertEqual(self.eventSender, None)
        Application.onPageRename -= self.__onPageRename

    def testInvalidRename(self):
        def rename(page, newtitle):
            page.title = newtitle

        self.assertRaises(DuplicateTitle, rename,
                          self.wikiroot["Страница 1"], "СтраНица 6")

    def testRename2(self):
        page = self.wikiroot["Страница 2/Страница 3"]
        page.title = "Страница 3 new"

        self.assertEqual(page.title, "Страница 3 new")
        self.assertEqual(self.wikiroot["Страница 2/Страница 3 new"], page)
        self.assertEqual(page.subpath, "Страница 2/Страница 3 new")
        self.assertEqual(self.wikiroot["Страница 2/Страница 3"], None)

    def testRename3(self):
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = page3["Страница 4"]

        page3.title = "Страница 3 new"

        self.assertEqual(page3["Страница 4"], page4)
        self.assertEqual(
            self.wikiroot["Страница 2/Страница 3 new/Страница 4"],
            page4
        )

    def testRename4(self):
        page = self.wikiroot["Страница 1"]
        page.title = "СтрАницА 1"

        self.assertEqual(page.title, "СтрАницА 1")
        self.assertEqual(self.wikiroot["СтрАницА 1"], page)
        self.assertEqual(page.subpath, "СтрАницА 1")

    def testLoad(self):
        page = self.wikiroot["Страница 1"]
        page.title = "Страница 1 new"

        wiki = WikiDocument.load(self.path)
        self.assertNotEqual(wiki["Страница 1 new"], None)
        self.assertEqual(wiki["Страница 1"], None)

    def testBookmarks1(self):
        page = self.wikiroot["Страница 6"]
        self.wikiroot.bookmarks.add(page)
        page.title = "Страница 6 new"

        self.assertTrue(self.wikiroot.bookmarks.pageMarked(page))

    def testBookmarks2(self):
        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.wikiroot.bookmarks.add(page2)
        self.wikiroot.bookmarks.add(page3)
        self.wikiroot.bookmarks.add(page4)

        page2.title = "Страница 2 new"

        self.assertTrue(self.wikiroot.bookmarks.pageMarked(page2))
        self.assertTrue(self.wikiroot.bookmarks.pageMarked(page3))
        self.assertTrue(self.wikiroot.bookmarks.pageMarked(page4))

    def testPath(self):
        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        page2.title = "Страница 2 new"

        self.assertEqual(page2.path,
                         os.path.join(self.path, "Страница 2 new"))
        self.assertEqual(page3.path,
                         os.path.join(self.path,
                                      "Страница 2 new",
                                      "Страница 3")
                         )
        self.assertEqual(page4.path,
                         os.path.join(self.path,
                                      "Страница 2 new",
                                      "Страница 3",
                                      "Страница 4")
                         )

    def testConfig(self):
        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        page2.title = "Страница 2 new"

        page2.tags = ["тег 1"]
        page3.tags = ["тег 2"]
        page4.tags = ["тег 3"]

        self.assertEqual(page2.tags[0], "тег 1")
        self.assertEqual(page3.tags[0], "тег 2")
        self.assertEqual(page4.tags[0], "тег 3")

    def testRenameError(self):
        page = self.wikiroot["Страница 2"]
        attach = Attachment(page)

        with open(attach.getFullPath("111.txt", True), "w"):
            try:
                page.title = "Новое имя"
            except OSError:
                pass
            else:
                self.assertTrue(
                    os.path.exists(self.wikiroot["Новое имя"].path)
                )
                self.assertEqual(self.wikiroot["Страница 2"], None)

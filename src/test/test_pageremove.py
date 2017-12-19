# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir


class RemovePagesTest(unittest.TestCase):
    def setUp(self):
        self.path = mkdtemp(prefix='Абырвалг абыр')
        Application.wikiroot = None

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])
        factory.create(self.wikiroot["Страница 1"],
                       "Страница 5",
                       [])
        factory.create(self.wikiroot,
                       "Страница 6",
                       [])

        self.pageRemoveCount = 0
        Application.wikiroot = None


    def tearDown(self):
        Application.wikiroot = None
        removeDir(self.path)


    def onPageRemove(self, bookmarks):
        """
        Обработка события при удалении страницы
        """
        self.pageRemoveCount += 1


    def testRemove1(self):
        Application.onPageRemove += self.onPageRemove
        Application.wikiroot = self.wikiroot

        # Удаляем страницу из корня
        page6 = self.wikiroot["Страница 6"]
        page6.remove()
        self.assertEqual(len(self.wikiroot), 2)
        self.assertEqual(self.wikiroot["Страница 6"], None)
        self.assertTrue(page6.isRemoved)
        self.assertEqual(self.pageRemoveCount, 1)

        # Удаляем подстраницу
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        page3.remove()

        self.assertEqual(len(self.wikiroot["Страница 2"]), 0)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 4"],
                         None)
        self.assertTrue(page3.isRemoved)
        self.assertTrue(page4.isRemoved)
        self.assertEqual(self.pageRemoveCount, 3)

        Application.onPageRemove -= self.onPageRemove


    def testRemove2(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 2"]

        self.wikiroot["Страница 2"].remove()

        self.assertEqual(Application.selectedPage, None)


    def testRemove3(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.wikiroot["Страница 2"].remove()

        self.assertEqual(Application.selectedPage, None)


    def testRemove4(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        self.wikiroot["Страница 2"].remove()

        self.assertEqual(Application.selectedPage, None)


    def testRemoveNoEvent(self):
        Application.onPageRemove += self.onPageRemove

        # Удаляем страницу из корня
        page6 = self.wikiroot["Страница 6"]
        page6.remove()
        self.assertEqual(len(self.wikiroot), 2)
        self.assertEqual(self.wikiroot["Страница 6"], None)
        self.assertTrue(page6.isRemoved)
        self.assertEqual(self.pageRemoveCount, 0)

        Application.onPageRemove -= self.onPageRemove


    def testIsRemoved(self):
        """
        Провкерка свойства isRemoved
        """
        page6 = self.wikiroot["Страница 6"]
        page6.remove()
        self.assertTrue(page6.isRemoved)

        # Удаляем подстраницу
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        page3.remove()

        self.assertTrue(page3.isRemoved)
        self.assertTrue(page4.isRemoved)

        self.assertFalse(self.wikiroot["Страница 2"].isRemoved)

    def testRemoveSelectedPage1(self):
        """
        Удаление выбранной страницы
        """
        # Если удаляется страница из корня, то никакая страница не выбирается
        self.wikiroot.selectedPage = self.wikiroot["Страница 6"]
        self.wikiroot["Страница 6"].remove()

        self.assertEqual(self.wikiroot.selectedPage, None)

        # Если удаляется страница более глубокая,
        # то выбранной страницей становится родитель
        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.wikiroot.selectedPage.remove()
        self.assertEqual(self.wikiroot.selectedPage,
                         self.wikiroot["Страница 2/Страница 3"])


    def testRemoveSelectedPage2(self):
        """
        Удаление выбранной страницы
        """
        # Если удаляется страница более глубокая,
        # то выбранной страницей становится родитель
        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.wikiroot.selectedPage.remove()
        self.assertEqual(self.wikiroot.selectedPage,
                         self.wikiroot["Страница 2/Страница 3"])


    def testRemoveFromBookmarks1(self):
        """
        Проверка того, что страница удаляется из закладок
        """
        page = self.wikiroot["Страница 6"]
        self.wikiroot.bookmarks.add(page)
        page.remove()

        self.assertFalse(self.wikiroot.bookmarks.pageMarked(page))


    def testRemoveFromBookmarks2(self):
        """
        Проверка того, что подстраница удаленной страницы удаляется из закладок
        """
        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.wikiroot.bookmarks.add(page2)
        self.wikiroot.bookmarks.add(page3)
        self.wikiroot.bookmarks.add(page4)

        page2.remove()

        self.assertFalse(self.wikiroot.bookmarks.pageMarked(page2))
        self.assertFalse(self.wikiroot.bookmarks.pageMarked(page3))
        self.assertFalse(self.wikiroot.bookmarks.pageMarked(page4))


    def testRemoveError1(self):
        page = self.wikiroot["Страница 2"]
        pagepath = page.path

        attach = Attachment(page)
        attachname = "add.png"
        attach.attach([os.path.join("../test/samplefiles", attachname)])

        with open(attach.getFullPath("111.txt", True), "w"):
            try:
                page.remove()
            except IOError:
                self.assertTrue(os.path.exists(pagepath))
                self.assertNotEqual(self.wikiroot["Страница 2"], None)
                self.assertTrue(
                    os.path.exists(self.wikiroot["Страница 2"].path)
                )
                self.assertEqual(len(self.wikiroot), 3)
                self.assertNotEqual(self.wikiroot["Страница 2/Страница 3"],
                                    None)
                self.assertNotEqual(
                    self.wikiroot["Страница 2/Страница 3/Страница 4"],
                    None
                )
            else:
                self.assertEqual(self.wikiroot["Страница 2"], None)
                self.assertFalse(os.path.exists(pagepath))


    def testRemoveError2(self):
        page1 = self.wikiroot["Страница 2"]
        page2 = self.wikiroot["Страница 2/Страница 3"]

        pagepath = page1.path

        attach2 = Attachment(page2)
        attachname = "add.png"
        attach2.attach([os.path.join("../test/samplefiles", attachname)])

        with open(attach2.getFullPath("111.txt", True), "w"):
            try:
                page1.remove()
            except IOError:
                self.assertTrue(os.path.exists(pagepath))
                self.assertNotEqual(self.wikiroot["Страница 2"], None)
                self.assertTrue(
                    os.path.exists(self.wikiroot["Страница 2"].path)
                )
                self.assertEqual(len(self.wikiroot), 3)
                self.assertNotEqual(self.wikiroot["Страница 2/Страница 3"],
                                    None)
                self.assertNotEqual(
                    self.wikiroot["Страница 2/Страница 3/Страница 4"],
                    None)
            else:
                self.assertEqual(self.wikiroot["Страница 2"], None)
                self.assertFalse(os.path.exists(pagepath))

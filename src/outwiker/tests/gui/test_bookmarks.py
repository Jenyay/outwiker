# -*- coding: utf-8 -*-

import unittest

from outwiker.app.actions.addbookmark import AddBookmarkAction
from outwiker.gui.defines import MENU_BOOKMARKS
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class BookmarksGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication(enableActionsGui=True)
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        self.bookmarks = self.application.bookmarks

    def tearDown(self):
        self.application.wikiroot = None
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testClearMenu(self):
        self.application.wikiroot = self.wikiroot
        self.application.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.assertNotEqual(bookmarksMenu, None)
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

    def _getItemText(self, item):
        return item.GetItemLabel().replace("_", "").replace("&", "")

    def testAddBookmarks1_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

    def testAddBookmarks1_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

    def testAddBookmarks2_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        newitems = bookmarksMenu.GetMenuItems()
        self.assertFalse(newitems[0].IsSeparator())
        self.assertTrue(newitems[1].IsSeparator())

        self.assertEqual(self._getItemText(newitems[2]), "Страница 3 [Страница 2]")

    def testAddBookmarks2_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        newitems = bookmarksMenu.GetMenuItems()
        self.assertFalse(newitems[0].IsSeparator())
        self.assertTrue(newitems[1].IsSeparator())

        self.assertEqual(self._getItemText(newitems[2]), "Страница 3 [Страница 2]")

    def testTitleBookmarks_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)
        self.bookmarks.add(
            self.wikiroot["Страница 2/Страница 3/Страница 4"], subpath=True
        )

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testTitleBookmarks_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testLoading_AsSubpath(self):
        self.bookmarks.setWikiRoot(self.wikiroot)
        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)
        self.bookmarks.add(
            self.wikiroot["Страница 2/Страница 3/Страница 4"], subpath=True
        )

        self.application.wikiroot = self.wikiroot

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        items = bookmarksMenu.GetMenuItems()
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testLoading_AsPageUID(self):
        self.bookmarks.setWikiRoot(self.wikiroot)
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.wikiroot = self.wikiroot

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        items = bookmarksMenu.GetMenuItems()
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testAddBookmarkAction1(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        self.application.selectedPage = self.wikiroot["Страница 1"]

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(
            None
        )

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)
        self.assertEqual(
            self._getItemText(bookmarksMenu.GetMenuItems()[2]), "Страница 1"
        )

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(
            None
        )
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

    def testEnableDisable(self):
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.assertFalse(bookmarksMenu.GetMenuItems()[0].IsEnabled())

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.assertFalse(bookmarksMenu.GetMenuItems()[0].IsEnabled())

        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.assertTrue(bookmarksMenu.GetMenuItems()[0].IsEnabled())

        self.application.selectedPage = None

        self.assertFalse(bookmarksMenu.GetMenuItems()[0].IsEnabled())

    def testRename1_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page = self.wikiroot["Страница 1"]
        self.bookmarks.add(page, subpath=True)
        page.title = "Страница 6 new"

        self.assertTrue(self.bookmarks.pageMarked(page))

    def testRename1_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page = self.wikiroot["Страница 1"]
        self.bookmarks.add(page)
        page.title = "Страница 6 new"

        self.assertTrue(self.bookmarks.pageMarked(page))

    def testRename2_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.bookmarks.add(page2, subpath=True)
        self.bookmarks.add(page3, subpath=True)
        self.bookmarks.add(page4, subpath=True)

        page2.title = "Страница 2 new"

        self.assertTrue(self.bookmarks.pageMarked(page2))
        self.assertTrue(self.bookmarks.pageMarked(page3))
        self.assertTrue(self.bookmarks.pageMarked(page4))

    def testRename2_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.bookmarks.add(page2)
        self.bookmarks.add(page3)
        self.bookmarks.add(page4)

        page2.title = "Страница 2 new"

        self.assertTrue(self.bookmarks.pageMarked(page2))
        self.assertTrue(self.bookmarks.pageMarked(page3))
        self.assertTrue(self.bookmarks.pageMarked(page4))

    def testRemove1_AsSubpath(self):
        """
        Проверка того, что страница удаляется из закладок
        """
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page = self.wikiroot["Страница 1"]
        self.bookmarks.add(page, subpath=True)
        page.remove()

        self.assertFalse(self.bookmarks.pageMarked(page))

    def testRemove1_AsPageUID(self):
        """
        Проверка того, что страница удаляется из закладок
        """
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page = self.wikiroot["Страница 1"]
        self.bookmarks.add(page)
        page.remove()

        self.assertFalse(self.bookmarks.pageMarked(page))

    def testRemove2_AsSubpath(self):
        """
        Проверка того, что подстраница удаленной страницы удаляется из закладок
        """
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.bookmarks.add(page2, subpath=True)
        self.bookmarks.add(page3, subpath=True)
        self.bookmarks.add(page4, subpath=True)

        page2.remove()

        self.assertFalse(self.bookmarks.pageMarked(page2))
        self.assertFalse(self.bookmarks.pageMarked(page3))
        self.assertFalse(self.bookmarks.pageMarked(page4))

    def testRemove2_AsPageUID(self):
        """
        Проверка того, что подстраница удаленной страницы удаляется из закладок
        """
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)

        page2 = self.wikiroot["Страница 2"]
        page3 = self.wikiroot["Страница 2/Страница 3"]
        page4 = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.bookmarks.add(page2)
        self.bookmarks.add(page3)
        self.bookmarks.add(page4)

        page2.remove()

        self.assertFalse(self.bookmarks.pageMarked(page2))
        self.assertFalse(self.bookmarks.pageMarked(page3))
        self.assertFalse(self.bookmarks.pageMarked(page4))

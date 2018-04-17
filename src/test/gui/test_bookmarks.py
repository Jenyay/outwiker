# -*- coding: utf-8 -*-

import unittest

from outwiker.actions.addbookmark import AddBookmarkAction
from outwiker.gui.defines import MENU_BOOKMARKS
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class BookmarksGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testClearMenu(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.assertNotEqual(bookmarksMenu, None)
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

    def _getItemText(self, item):
        return item.GetText().replace("_", "").replace("&", "")

    def testAddBookmarks1(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")

        self.wikiroot.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

    def testAddBookmarks2(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]),
                         "Страница 3 [Страница 2]")

        self.wikiroot.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        newitems = bookmarksMenu.GetMenuItems()
        self.assertFalse(newitems[0].IsSeparator())
        self.assertTrue(newitems[1].IsSeparator())

        self.assertEqual(self._getItemText(newitems[2]),
                         "Страница 3 [Страница 2]")

    def testTitleBookmarks(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[0].IsSeparator())
        self.assertTrue(items[1].IsSeparator())

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]")

    def testLoading(self):
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 1"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.wikiroot.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.wikiroot = self.wikiroot

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        items = bookmarksMenu.GetMenuItems()
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        self.assertEqual(self._getItemText(items[2]), "Страница 1")
        self.assertEqual(self._getItemText(items[3]), "Страница 3 [Страница 2]")
        self.assertEqual(self._getItemText(items[4]), "Страница 4 [Страница 2/Страница 3]")

    def testAddBookmarkAction1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 2)

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(None)

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)
        self.assertEqual(self._getItemText(bookmarksMenu.GetMenuItems()[2]),
                         "Страница 1")

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(None)
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

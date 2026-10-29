# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.app.actions.addbookmark import AddBookmarkAction
from outwiker.app.gui.dialogs.bookmarksdialog import (
    BookmarksDialog,
    BookmarksDialogController,
)
from outwiker.gui.defines import MENU_BOOKMARKS
from outwiker.gui.guiconfig import BookmarksDialogConfig
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
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

    def _getItemText(self, item):
        return item.GetItemLabel().replace("_", "").replace("&", "")

    def testAddBookmarks1_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

    def testAddBookmarks1_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

    def testAddBookmarks2_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        newitems = bookmarksMenu.GetMenuItems()
        self.assertFalse(newitems[1].IsSeparator())
        self.assertTrue(newitems[2].IsSeparator())

        self.assertEqual(self._getItemText(newitems[3]), "Страница 3 [Страница 2]")

    def testAddBookmarks2_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 5)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")

        self.bookmarks.remove(self.wikiroot["Страница 1"])
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)

        newitems = bookmarksMenu.GetMenuItems()
        self.assertFalse(newitems[1].IsSeparator())
        self.assertTrue(newitems[2].IsSeparator())

        self.assertEqual(self._getItemText(newitems[3]), "Страница 3 [Страница 2]")

    def testTitleBookmarks_AsSubpath(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"], subpath=True)
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"], subpath=True)
        self.bookmarks.add(
            self.wikiroot["Страница 2/Страница 3/Страница 4"], subpath=True
        )

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 6)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[5]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testTitleBookmarks_AsPageUID(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]

        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 6)

        items = bookmarksMenu.GetMenuItems()
        self.assertFalse(items[1].IsSeparator())
        self.assertTrue(items[2].IsSeparator())

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[5]), "Страница 4 [Страница 2/Страница 3]"
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
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 6)

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[5]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testLoading_AsPageUID(self):
        self.bookmarks.setWikiRoot(self.wikiroot)
        self.bookmarks.add(self.wikiroot["Страница 1"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3"])
        self.bookmarks.add(self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.wikiroot = self.wikiroot

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        items = bookmarksMenu.GetMenuItems()
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 6)

        self.assertEqual(self._getItemText(items[3]), "Страница 1")
        self.assertEqual(self._getItemText(items[4]), "Страница 3 [Страница 2]")
        self.assertEqual(
            self._getItemText(items[5]), "Страница 4 [Страница 2/Страница 3]"
        )

    def testAddBookmarkAction1(self):
        self.application.wikiroot = self.wikiroot
        self.bookmarks.setWikiRoot(self.wikiroot)
        self.application.selectedPage = self.wikiroot["Страница 1"]

        bookmarksMenu = self.mainWindow.menuController[MENU_BOOKMARKS]
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(
            None
        )

        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 4)
        self.assertEqual(
            self._getItemText(bookmarksMenu.GetMenuItems()[3]), "Страница 1"
        )

        self.application.actionController.getAction(AddBookmarkAction.stringId).run(
            None
        )
        self.assertEqual(bookmarksMenu.GetMenuItemCount(), 3)

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


class BookmarksDialogSizeTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.application.wikiroot = None
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _createDialog(self):
        dialog = BookmarksDialog(self.mainWindow, self.application.theme)
        controller = BookmarksDialogController(dialog, self.application)
        return dialog, controller

    def testDefaultSize(self):
        dialog, _ = self._createDialog()
        self.assertEqual(tuple(dialog.GetSize()), (500, 350))

    def testSaveSizeOnCloseButton(self):
        dialog, _ = self._createDialog()
        dialog.Show()
        dialog.SetSize(wx.Size(612, 423))

        dialog.close_btn.ProcessEvent(
            wx.CommandEvent(wx.EVT_BUTTON.typeId, wx.ID_CLOSE)
        )

        self.assertFalse(dialog.IsShown())

        config = BookmarksDialogConfig(self.application.config)
        self.assertEqual(config.width.value, 612)
        self.assertEqual(config.height.value, 423)

    def testSaveSizeOnCloseEvent(self):
        dialog, _ = self._createDialog()
        dialog.Show()
        dialog.SetSize(wx.Size(612, 423))

        dialog.Close()

        self.assertFalse(dialog.IsShown())

        config = BookmarksDialogConfig(self.application.config)
        self.assertEqual(config.width.value, 612)
        self.assertEqual(config.height.value, 423)

    def testLoadSavedSize(self):
        config = BookmarksDialogConfig(self.application.config)
        config.width.value = 640
        config.height.value = 480

        dialog, _ = self._createDialog()
        self.assertEqual(tuple(dialog.GetSize()), (640, 480))

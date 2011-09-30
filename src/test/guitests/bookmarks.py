#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from test.utils import removeWiki


class BookmarksGuiTest (BaseMainWndTest):
	def setUp (self):
		BaseMainWndTest.setUp (self)

		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])



	def tearDown (self):
		BaseMainWndTest.tearDown (self)
		Application.wikiroot = None
		removeWiki (self.path)


	def testClearMenu (self):
		Application.wikiroot = self.rootwiki
		bookmarksMenu = self.wnd.mainMenu.bookmarksMenu

		self.assertNotEqual (bookmarksMenu, None)
		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 2)

		items = bookmarksMenu.GetMenuItems()
		self.assertFalse (items[0].IsSeparator())
		self.assertTrue (items[1].IsSeparator())


	def testAddBookmarks1 (self):
		Application.wikiroot = self.rootwiki
		bookmarksMenu = self.wnd.mainMenu.bookmarksMenu

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 3)

		items = bookmarksMenu.GetMenuItems()
		self.assertFalse (items[0].IsSeparator())
		self.assertTrue (items[1].IsSeparator())

		self.assertEqual (items[2].GetText(), u"Страница 1")

		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 1"])
		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 2)


	def testAddBookmarks2 (self):
		Application.wikiroot = self.rootwiki
		bookmarksMenu = self.wnd.mainMenu.bookmarksMenu

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 4)

		items = bookmarksMenu.GetMenuItems()
		self.assertFalse (items[0].IsSeparator())
		self.assertTrue (items[1].IsSeparator())

		self.assertEqual (items[2].GetText(), u"Страница 1")
		self.assertEqual (items[3].GetText(), u"Страница 3 [Страница 2]")

		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 1"])
		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 3)

		newitems = bookmarksMenu.GetMenuItems()
		self.assertFalse (items[0].IsSeparator())
		self.assertTrue (items[1].IsSeparator())

		self.assertEqual (items[2].GetText(), u"Страница 3 [Страница 2]")


	def testTitleBookmarks (self):
		Application.wikiroot = self.rootwiki
		bookmarksMenu = self.wnd.mainMenu.bookmarksMenu

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3/Страница 4"])

		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 5)

		items = bookmarksMenu.GetMenuItems()
		self.assertFalse (items[0].IsSeparator())
		self.assertTrue (items[1].IsSeparator())

		self.assertEqual (items[2].GetText(), u"Страница 1")
		self.assertEqual (items[3].GetText(), u"Страница 3 [Страница 2]")
		self.assertEqual (items[4].GetText(), u"Страница 4 [Страница 2/Страница 3]")


	def testLoading (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3/Страница 4"])

		Application.wikiroot = self.rootwiki

		bookmarksMenu = self.wnd.mainMenu.bookmarksMenu
		items = bookmarksMenu.GetMenuItems()
		self.assertEqual (bookmarksMenu.GetMenuItemCount(), 5)

		self.assertEqual (items[2].GetText(), u"Страница 1")
		self.assertEqual (items[3].GetText(), u"Страница 3 [Страница 2]")
		self.assertEqual (items[4].GetText(), u"Страница 4 [Страница 2/Страница 3]")

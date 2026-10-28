# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.tree import WikiPage
from outwiker.gui.controls.pagelist import PageList
from outwiker.gui.controls.pagelist_columns import ColumnsFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class PageListSetItemPositionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self._createPages(["A", "B", "C", "D", "E"])

        self.pagelist = PageList(self.mainWindow)
        self.pagelist.setColumns(ColumnsFactory().createDefaultColumns())
        self.pagelist.setPageList(self.pages)

    def tearDown(self):
        wx.SafeYield()
        self.pagelist.Destroy()
        self.application.wikiroot = None
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _createPages(self, titles):
        factory = TextPageFactory()
        self.pages = [factory.create(self.wikiroot, title, []) for title in titles]

    def _getTitles(self) -> list[str]:
        return [
            self.pagelist.listCtrl.GetItemText(index)
            for index in range(self.pagelist.listCtrl.GetItemCount())
        ]

    def _getPages(self) -> list[WikiPage]:
        return [
            self.pagelist.listCtrl.GetItemData(index)
            for index in range(self.pagelist.listCtrl.GetItemCount())
        ]

    def testInitialOrder(self):
        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
        self.assertEqual(self._getPages(), self.pages)

    def testMoveDown(self):
        self.pagelist.setItemPosition(1, 3)
        self.assertEqual(self._getTitles(), ["A", "C", "D", "B", "E"])

        pages = self._getPages()
        self.assertEqual(pages, [self.pages[0], self.pages[2],
                                 self.pages[3], self.pages[1], self.pages[4]])

    def testMoveUp(self):
        self.pagelist.setItemPosition(3, 1)
        self.assertEqual(self._getTitles(), ["A", "D", "B", "C", "E"])

        pages = self._getPages()
        self.assertEqual(pages, [self.pages[0], self.pages[3],
                                 self.pages[1], self.pages[2], self.pages[4]])

    def testMoveToEnd(self):
        self.pagelist.setItemPosition(0, 4)
        self.assertEqual(self._getTitles(), ["B", "C", "D", "E", "A"])

    def testMoveToStart(self):
        self.pagelist.setItemPosition(4, 0)
        self.assertEqual(self._getTitles(), ["E", "A", "B", "C", "D"])

    def testMoveNeighbour(self):
        self.pagelist.setItemPosition(2, 3)
        self.assertEqual(self._getTitles(), ["A", "B", "D", "C", "E"])

        self.pagelist.setItemPosition(3, 2)
        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])

    def testMoveToSamePosition(self):
        self.pagelist.setItemPosition(2, 2)
        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
        self.assertEqual(self._getPages(), self.pages)

    def testInvalidSrcPosition(self):
        for position in [-1, 5, 100, -100]:
            self.pagelist.setItemPosition(position, 1)
            self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
            self.assertEqual(self._getPages(), self.pages)

    def testInvalidNewPosition(self):
        for position in [-1, 5, 100, -100]:
            self.pagelist.setItemPosition(1, position)
            self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
            self.assertEqual(self._getPages(), self.pages)

    def testEmptyList(self):
        self.pagelist.setPageList([])
        self.pagelist.setItemPosition(0, 0)
        self.assertEqual(self.pagelist.listCtrl.GetItemCount(), 0)

    def testInternalPagesOrder(self):
        self.pagelist.setItemPosition(1, 3)
        self.assertEqual(
            self.pagelist._pages,
            [self.pages[0], self.pages[2], self.pages[3], self.pages[1],
             self.pages[4]],
        )

        self.pagelist.setItemPosition(4, 0)
        self.assertEqual(
            self.pagelist._pages,
            [self.pages[4], self.pages[0], self.pages[2], self.pages[3],
             self.pages[1]],
        )

    def testInternalPagesOrderAfterInvalidMove(self):
        self.pagelist.setItemPosition(-1, 2)
        self.pagelist.setItemPosition(2, 5)
        self.assertEqual(self.pagelist._pages, self.pages)

    def testOrderIsKeptAfterColumnsUpdate(self):
        self.pagelist.setItemPosition(0, 4)
        self.pagelist.setColumns(ColumnsFactory().createDefaultColumns())
        self.assertEqual(self._getTitles(), ["B", "C", "D", "E", "A"])

        pages = self._getPages()
        self.assertEqual(pages, [self.pages[1], self.pages[2],
                                 self.pages[3], self.pages[4], self.pages[0]])

    def testSelectedItemStaysSelectedAfterMoveDown(self):
        self.pagelist.setSelected(1)
        self.pagelist.setItemPosition(1, 3)

        self.assertEqual(self._getTitles(), ["A", "C", "D", "B", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 3)

    def testSelectedItemStaysSelectedAfterMoveUp(self):
        self.pagelist.setSelected(4)
        self.pagelist.setItemPosition(4, 0)

        self.assertEqual(self._getTitles(), ["E", "A", "B", "C", "D"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 0)

    def testOnlyMovedItemIsSelected(self):
        self.pagelist.setSelected(2)
        self.pagelist.setItemPosition(2, 4)

        selected = [
            self.pagelist.listCtrl.IsSelected(index)
            for index in range(self.pagelist.listCtrl.GetItemCount())
        ]
        self.assertEqual(selected, [False, False, False, False, True])

    def testSelectionDoesNotChangeIfMovedItemIsNotSelected(self):
        self.pagelist.setSelected(0)
        self.pagelist.setItemPosition(2, 4)

        self.assertEqual(self._getTitles(), ["A", "B", "D", "E", "C"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 0)

    def testNoSelectionAfterMove(self):
        self.pagelist.setItemPosition(1, 3)

        self.assertEqual(self._getTitles(), ["A", "C", "D", "B", "E"])
        self.assertIsNone(self.pagelist.getSelectedIndex())

    def testMoveSelectedItemUp(self):
        self.pagelist.setSelected(2)
        self.pagelist.moveSelectedItemUp()

        self.assertEqual(self._getTitles(), ["A", "C", "B", "D", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 1)

    def testMoveSelectedItemDown(self):
        self.pagelist.setSelected(2)
        self.pagelist.moveSelectedItemDown()

        self.assertEqual(self._getTitles(), ["A", "B", "D", "C", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 3)

    def testMoveSelectedItemUpTwice(self):
        self.pagelist.setSelected(3)
        self.pagelist.moveSelectedItemUp()
        self.pagelist.moveSelectedItemUp()

        self.assertEqual(self._getTitles(), ["A", "D", "B", "C", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 1)

    def testMoveSelectedItemDownTwice(self):
        self.pagelist.setSelected(1)
        self.pagelist.moveSelectedItemDown()
        self.pagelist.moveSelectedItemDown()

        self.assertEqual(self._getTitles(), ["A", "C", "D", "B", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 3)

    def testMoveSelectedItemUpFromFirstPosition(self):
        self.pagelist.setSelected(0)
        self.pagelist.moveSelectedItemUp()

        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 0)

    def testMoveSelectedItemDownFromLastPosition(self):
        self.pagelist.setSelected(4)
        self.pagelist.moveSelectedItemDown()

        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
        self.assertEqual(self.pagelist.getSelectedIndex(), 4)

    def testMoveSelectedItemWithoutSelection(self):
        self.pagelist.moveSelectedItemUp()
        self.pagelist.moveSelectedItemDown()

        self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
        self.assertIsNone(self.pagelist.getSelectedIndex())

    def testMoveSelectedItemInEmptyList(self):
        self.pagelist.setPageList([])
        self.pagelist.moveSelectedItemUp()
        self.pagelist.moveSelectedItemDown()

        self.assertEqual(self.pagelist.listCtrl.GetItemCount(), 0)

    def testRemoveItem(self):
        self.pagelist.removeItem(2)

        self.assertEqual(self._getTitles(), ["A", "B", "D", "E"])
        self.assertEqual(self._getPages(), [self.pages[0], self.pages[1],
                                            self.pages[3], self.pages[4]])
        self.assertEqual(self.pagelist._pages, [self.pages[0], self.pages[1],
                                                self.pages[3], self.pages[4]])

    def testRemoveFirstItem(self):
        self.pagelist.removeItem(0)
        self.assertEqual(self._getTitles(), ["B", "C", "D", "E"])
        self.assertEqual(self.pagelist._pages, self.pages[1:])

    def testRemoveLastItem(self):
        self.pagelist.removeItem(4)
        self.assertEqual(self._getTitles(), ["A", "B", "C", "D"])
        self.assertEqual(self.pagelist._pages, self.pages[:4])

    def testRemoveInvalidIndex(self):
        for index in [-1, 5, 100, -100]:
            self.pagelist.removeItem(index)
            self.assertEqual(self._getTitles(), ["A", "B", "C", "D", "E"])
            self.assertEqual(self.pagelist._pages, self.pages)

    def testRemoveItemFromEmptyList(self):
        self.pagelist.setPageList([])
        self.pagelist.removeItem(0)
        self.assertEqual(self.pagelist.listCtrl.GetItemCount(), 0)

    def testRemoveSelectedItem(self):
        self.pagelist.setSelected(2)
        self.pagelist.removeItem(2)

        self.assertEqual(self._getTitles(), ["A", "B", "D", "E"])
        self.assertIsNone(self.pagelist.getSelectedIndex())

    def testRemoveAllItems(self):
        for _ in range(5):
            self.pagelist.removeItem(0)

        self.assertEqual(self.pagelist.listCtrl.GetItemCount(), 0)
        self.assertEqual(self.pagelist._pages, [])

    def testTitleIsHypertext(self):
        self.pagelist.setItemPosition(0, 2)
        self.assertTrue(self.pagelist.listCtrl.IsItemHyperText(2, 0))

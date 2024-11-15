# -*- coding: utf-8 -*-

import os
from typing import List
import unittest

import wx

from outwiker.core.tree import BasePage
from outwiker.gui.controls.notestreectrl2 import NotesTreeItem
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class TreeTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _getTreeCtrl(self):
        return self.mainWindow.treePanel.panel.treeCtrl

    def _getChildrenRecursive(self, item: NotesTreeItem) -> List[NotesTreeItem]:
        children = []
        self._addChildrenToList(item, children)
        return children

    def _getChildrenCountRecursive(self, item: NotesTreeItem) -> int:
        return len(self._getChildrenRecursive(item))

    def _addChildrenToList(self, item: NotesTreeItem, children: List[NotesTreeItem]) -> None:
        children += item.getChildren()
        for child in item.getChildren():
            self._addChildrenToList(child, children)

    def testTreeExists(self):
        tree = self._getTreeCtrl()
        self.assertNotEqual(tree, None)

    def testTreeItems(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(
            self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(
            self.wikiroot["Страница 2/Страница 3/Страница 4"], "Страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        factory.create(
            self.wikiroot["Страница 1/Страница 5"], "Страница 7", [])

        self.application.wikiroot = self.wikiroot
        tree = self._getTreeCtrl()

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

    def testExpand(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 2/Страница 3/Страница 4"], "Страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        factory.create(self.wikiroot["Страница 1/Страница 5"], "Страница 7", [])

        self.application.wikiroot = self.wikiroot
        tree = self._getTreeCtrl()

        # Разворот 1
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        tree.expand(self.wikiroot["Страница 1"])
        wx.SafeYield()
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        # Разворот 2
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        tree.expand(self.wikiroot["Страница 2"])
        wx.SafeYield()

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        # Разворот 3
        tree.expand(self.wikiroot["Страница 2/Страница 3"])
        wx.SafeYield()

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

    def testExpandReadOnly(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 2/Страница 3/Страница 4"], "Страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        factory.create(self.wikiroot["Страница 1/Страница 5"], "Страница 7", [])

        self._setReadOnly(self.wikiroot, True)

        self.application.wikiroot = self.wikiroot
        tree = self._getTreeCtrl()

        # Разворот 1
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        tree.expand(self.wikiroot["Страница 1"])
        wx.SafeYield()
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        # Разворот 2
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        tree.expand(self.wikiroot["Страница 2"])
        wx.SafeYield()

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        # Разворот 3
        tree.expand(self.wikiroot["Страница 2/Страница 3"])
        wx.SafeYield()

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

    def testSelectCollapsed(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 2/Страница 3/Страница 4"], "Страница 6", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        factory.create(self.wikiroot["Страница 1/Страница 5"], "Страница 7", [])

        self.application.wikiroot = self.wikiroot
        tree = self._getTreeCtrl()

        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3"]), None)

        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

    def testTreeLoadingEmpty(self):
        tree = self._getTreeCtrl()

        self.application.wikiroot = self.wikiroot

        rootitem = tree.getRootItem(0)
        self.assertEqual(rootitem.getTitle(),
                          os.path.basename(self.wikiroot.path))
        self.assertEqual(rootitem.getChildrenCount(), 0)
        self.assertEqual(rootitem.getPage(), self.wikiroot)

    def testAddPage(self):
        tree = self._getTreeCtrl()

        self.application.wikiroot = self.wikiroot

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        rootitem = tree.getRootItem(0)
        childitem = rootitem.getChildren()[0]

        self.assertEqual(len(rootitem.getChildren()), 1)

        self.assertEqual(childitem.getTitle(), "Страница 1")
        self.assertEqual(len(childitem.getChildren()), 0)
        self.assertEqual(childitem.getPage(), self.wikiroot["Страница 1"])

    def testAddMorePages(self):
        tree = self._getTreeCtrl()

        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        rootitem = tree.getRootItem(0)
        self.assertEqual(self._getChildrenCountRecursive(rootitem), 5)
        self.assertEqual(rootitem.getChildrenCount(), 2)

        page2Item = rootitem.getChildren()[1]
        page3Item = page2Item.getChildren()[0]

        self.assertEqual(page2Item.getPage(), self.wikiroot["Страница 2"])
        self.assertEqual(page2Item.getTitle(), "Страница 2")
        self.assertEqual(page2Item.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(page2Item), 2)

        self.assertEqual(page3Item.getPage(), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(page3Item.getTitle(), "Страница 3")
        self.assertEqual(page3Item.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(page3Item), 1)

    def testRemovePage(self):
        tree = self._getTreeCtrl()

        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        rootitem = tree.getRootItem(0)
        self.assertEqual(rootitem.getChildrenCount(), 2)
        self.assertEqual(self._getChildrenCountRecursive(rootitem), 5)

        self.wikiroot["Страница 2/Страница 3"].remove()

        newrootitem = tree.getRootItem(0)
        self.assertEqual(newrootitem.getChildrenCount(), 2)
        self.assertEqual(self._getChildrenCountRecursive(newrootitem), 3)

        self.wikiroot["Страница 2"].remove()

        newrootitem2 = tree.getRootItem(0)
        self.assertEqual(newrootitem2.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(newrootitem2), 2)

    def testSelectedPage(self):
        tree = self._getTreeCtrl()

        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]

        selPage = tree.getSelectedPage()
        self.assertEqual(selPage, self.wikiroot.selectedPage)
        self.assertEqual(selPage, self.wikiroot["Страница 1"])

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        selPage = tree.getSelectedPage()
        self.assertEqual(selPage, self.wikiroot.selectedPage)
        self.assertEqual(selPage, self.wikiroot["Страница 2/Страница 3"])

    def testOrder1(self):
        tree = self._getTreeCtrl()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])
        self.wikiroot["Страница 2"].order -= 1

        self.application.wikiroot = self.wikiroot

        rootitem = tree.getRootItem(0)
        page2Item = rootitem.getChildren()[0]

        self.assertEqual(page2Item.getPage(), self.wikiroot["Страница 2"])
        self.assertEqual(page2Item.getTitle(), "Страница 2")
        self.assertEqual(page2Item.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(page2Item), 1)

        page3Item = page2Item.getChildren()[0]

        self.assertEqual(page3Item.getPage(), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(page3Item.getTitle(), "Страница 3")
        self.assertEqual(page3Item.getChildrenCount(), 0)
        self.assertEqual(self._getChildrenCountRecursive(page3Item), 0)

    def testOrder2(self):
        tree = self._getTreeCtrl()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.wikiroot["Страница 2"]

        selPage = tree.getSelectedPage()
        self.assertEqual(selPage, self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot.selectedPage, self.wikiroot["Страница 2"])

        self.application.wikiroot.selectedPage.order -= 1

        selPage = tree.getSelectedPage()
        self.assertEqual(selPage, self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot.selectedPage, self.wikiroot["Страница 2"])

        rootitem = tree.getRootItem(0)
        page2Item = rootitem.getChildren()[0]

        self.assertEqual(page2Item.getPage(), self.wikiroot["Страница 2"])
        self.assertEqual(page2Item.getTitle(), "Страница 2")
        self.assertEqual(page2Item.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(page2Item), 1)

        page3Item = page2Item.getChildren()[0]

        self.assertEqual(page3Item.getPage(), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(page3Item.getTitle(), "Страница 3")
        self.assertEqual(page3Item.getChildrenCount(), 0)
        self.assertEqual(self._getChildrenCountRecursive(page3Item), 0)

    def testRename(self):
        tree = self._getTreeCtrl()
        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.wikiroot["Страница 2"].title = "Переименованная страница"

        rootitem = tree.getRootItem(0)
        newPageItem = rootitem.getChildren()[1]

        self.assertEqual(newPageItem.getPage(), self.wikiroot["Переименованная страница"])
        self.assertEqual(newPageItem.getTitle(), "Переименованная страница")
        self.assertEqual(newPageItem.getChildrenCount(), 1)
        self.assertEqual(self._getChildrenCountRecursive(newPageItem), 2)

    def testInvalidIcon(self):
        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        page = factory.create(self.wikiroot, "Страница 1", [])
        icon_name = 'testdata/images/invalid.png'
        assert os.path.exists(icon_name)

        page.icon = icon_name

    def _setReadOnly(self, page: BasePage, readonly: bool = True):
        page.readonly = readonly
        for child in page.children:
            self._setReadOnly(child, readonly)

# -*- coding: utf-8 -*-

import os
import unittest

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
        tree = self.mainWindow.treePanel.panel

        # Разворот 1
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        tree.expand(self.wikiroot["Страница 1"])
        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 1/Страница 5/Страница 7"]), None)

        # Разворот 2
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        tree.expand(self.wikiroot["Страница 2"])

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        # Разворот 3
        tree.expand(self.wikiroot["Страница 2/Страница 3"])

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

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3/Страница 4"]), None)

        self.assertNotEqual(tree.getTreeItem(self.wikiroot["Страница 2/Страница 3"]), None)

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
        self.assertEqual(tree.GetChildrenCount(rootitem, True), 5)
        self.assertEqual(tree.GetChildrenCount(rootitem, False), 2)

        firstItem, cookie = tree.GetFirstChild(rootitem)
        page2Item = tree.GetNextSibling(firstItem)

        self.assertEqual(tree.GetChildrenCount(page2Item, True), 2)
        self.assertEqual(tree.GetChildrenCount(page2Item, False), 1)
        self.assertEqual(tree.GetItemData(page2Item), self.wikiroot["Страница 2"])
        self.assertEqual(tree.GetItemText(page2Item), "Страница 2")

        page3Item, cookie = tree.GetFirstChild(page2Item)

        self.assertEqual(tree.GetChildrenCount(page3Item, True), 1)
        self.assertEqual(tree.GetChildrenCount(page3Item, False), 1)
        self.assertEqual(tree.GetItemData(page3Item), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(tree.GetItemText(page3Item), "Страница 3")

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
        self.assertEqual(tree.GetChildrenCount(rootitem, True), 5)
        self.assertEqual(tree.GetChildrenCount(rootitem, False), 2)

        self.wikiroot["Страница 2/Страница 3"].remove()

        newrootitem = tree.getRootItem(0)
        self.assertEqual(tree.GetChildrenCount(newrootitem, True), 3)
        self.assertEqual(tree.GetChildrenCount(newrootitem, False), 2)

        self.wikiroot["Страница 2"].remove()

        newrootitem2 = tree.getRootItem(0)
        self.assertEqual(tree.GetChildrenCount(newrootitem2, True), 2)
        self.assertEqual(tree.GetChildrenCount(newrootitem2, False), 1)

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

        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.wikiroot["Страница 2"].order -= 1

        rootitem = tree.getRootItem(0)
        page2Item, cookie = tree.GetFirstChild(rootitem)

        self.assertEqual(tree.GetChildrenCount(page2Item, False), 1)
        self.assertEqual(tree.GetChildrenCount(page2Item, True), 1)
        self.assertEqual(tree.GetItemData(page2Item), self.wikiroot["Страница 2"])
        self.assertEqual(tree.GetItemText(page2Item), "Страница 2")

        page3Item, cookie = tree.GetFirstChild(page2Item)

        self.assertEqual(tree.GetChildrenCount(page3Item, True), 0)
        self.assertEqual(tree.GetChildrenCount(page3Item, False), 0)
        self.assertEqual(tree.GetItemData(page3Item), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(tree.GetItemText(page3Item), "Страница 3")

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

        selItem = tree.GetSelection()
        self.assertEqual(tree.GetItemData(selItem), self.wikiroot["Страница 2"])
        self.assertEqual(tree.GetItemData(selItem), self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot.selectedPage, self.wikiroot["Страница 2"])

        self.application.wikiroot.selectedPage.order -= 1

        selItem = tree.GetSelection()
        self.assertEqual(tree.GetItemData(selItem), self.wikiroot["Страница 2"])
        self.assertEqual(tree.GetItemData(selItem), self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot.selectedPage, self.wikiroot["Страница 2"])

        rootitem = tree.getRootItem(0)
        page2Item, cookie = tree.GetFirstChild(rootitem)

        self.assertEqual(tree.GetChildrenCount(page2Item, False), 1)
        self.assertEqual(tree.GetChildrenCount(page2Item, True), 1)
        self.assertEqual(tree.GetItemData(page2Item), self.wikiroot["Страница 2"])
        self.assertEqual(tree.GetItemText(page2Item), "Страница 2")

        page3Item, cookie = tree.GetFirstChild(page2Item)

        self.assertEqual(tree.GetChildrenCount(page3Item, False), 0)
        self.assertEqual(tree.GetChildrenCount(page3Item, True), 0)
        self.assertEqual(tree.GetItemData(page3Item), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(tree.GetItemText(page3Item), "Страница 3")

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
        firstItem = rootitem.getChildren()[0]
        newPageItem = rootitem.getChildren()[1]

        self.assertEqual(newPageItem.getPage(), self.wikiroot["Переименованная страница"])
        self.assertEqual(newPageItem.getTitle(), "Переименованная страница")
        self.assertEqual(tree.GetChildrenCount(newPageItem, False), 1)
        self.assertEqual(tree.GetChildrenCount(newPageItem, True), 2)

    def testInvalidIcon(self):
        tree = self._getTreeCtrl()
        self.application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        page = factory.create(self.wikiroot, "Страница 1", [])
        icon_name = 'testdata/images/invalid.png'
        assert os.path.exists(icon_name)

        page.icon = icon_name

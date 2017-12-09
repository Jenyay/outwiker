# -*- coding: UTF-8 -*-

import os

from basemainwnd import BaseMainWndTest
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application


class TreeTest (BaseMainWndTest):
    def _getTreeCtrl (self):
        return self.wnd.treePanel.panel.treeCtrl


    def testTreeExists (self):
        tree = self._getTreeCtrl()
        self.assertNotEqual (tree, None)


    def testTreeItems (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3/Страница 4"], u"Страница 6", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])
        factory.create (self.wikiroot[u"Страница 1/Страница 5"], u"Страница 7", [])

        Application.wikiroot = self.wikiroot
        tree = self.wnd.treePanel.panel

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 1"]), None)
        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2"]), None)
        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)
        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 1/Страница 5"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 1/Страница 5/Страница 7"]), None)


    def testExpand (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3/Страница 4"], u"Страница 6", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])
        factory.create (self.wikiroot[u"Страница 1/Страница 5"], u"Страница 7", [])

        Application.wikiroot = self.wikiroot
        tree = self.wnd.treePanel.panel


        # Разворот 1
        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 1/Страница 5"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 1/Страница 5/Страница 7"]), None)

        tree.expand (self.wikiroot[u"Страница 1"])
        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 1/Страница 5/Страница 7"]), None)


        # Разворот 2
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        tree.expand (self.wikiroot[u"Страница 2"])

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4"]), None)
        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)


        # Разворот 3
        tree.expand (self.wikiroot[u"Страница 2/Страница 3"])

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)


    def testSelectCollapsed (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3/Страница 4"], u"Страница 6", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])
        factory.create (self.wikiroot[u"Страница 1/Страница 5"], u"Страница 7", [])

        Application.wikiroot = self.wikiroot
        tree = self.wnd.treePanel.panel

        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        self.assertEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4"]), None)

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3"]), None)

        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4/Страница 6"]), None)

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3/Страница 4"]), None)

        self.assertNotEqual (tree.getTreeItem (self.wikiroot[u"Страница 2/Страница 3"]), None)


    def testTreeLoadingEmpty (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        rootitem = tree.GetRootItem()
        self.assertEqual (tree.GetItemText (rootitem),
                          os.path.basename (self.path))
        self.assertEqual (tree.GetChildrenCount (rootitem), 0)
        self.assertEqual (tree.GetItemData(rootitem), self.wikiroot)


    def testAddPage (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        rootitem = tree.GetRootItem()
        childitem, cookie = tree.GetFirstChild (rootitem)

        self.assertEqual (tree.GetChildrenCount (rootitem), 1)

        self.assertEqual (tree.GetItemText (childitem), u"Страница 1")
        self.assertEqual (tree.GetChildrenCount (childitem), 0)
        self.assertEqual (tree.GetItemData(childitem), self.wikiroot[u"Страница 1"])


    def testAddMorePages (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        rootitem = tree.GetRootItem()
        self.assertEqual (tree.GetChildrenCount (rootitem, True), 5)
        self.assertEqual (tree.GetChildrenCount (rootitem, False), 2)

        firstItem, cookie = tree.GetFirstChild (rootitem)
        page2Item = tree.GetNextSibling (firstItem)

        self.assertEqual (tree.GetChildrenCount (page2Item, True), 2)
        self.assertEqual (tree.GetChildrenCount (page2Item, False), 1)
        self.assertEqual (tree.GetItemData(page2Item), self.wikiroot[u"Страница 2"])
        self.assertEqual (tree.GetItemText (page2Item), u"Страница 2")

        page3Item, cookie = tree.GetFirstChild (page2Item)

        self.assertEqual (tree.GetChildrenCount (page3Item, True), 1)
        self.assertEqual (tree.GetChildrenCount (page3Item, False), 1)
        self.assertEqual (tree.GetItemData(page3Item), self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (tree.GetItemText (page3Item), u"Страница 3")


    def testRemovePage (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        rootitem = tree.GetRootItem()
        self.assertEqual (tree.GetChildrenCount (rootitem, True), 5)
        self.assertEqual (tree.GetChildrenCount (rootitem, False), 2)

        self.wikiroot[u"Страница 2/Страница 3"].remove()

        newrootitem = tree.GetRootItem()
        self.assertEqual (tree.GetChildrenCount (newrootitem, True), 3)
        self.assertEqual (tree.GetChildrenCount (newrootitem, False), 2)

        self.wikiroot[u"Страница 2"].remove()

        newrootitem2 = tree.GetRootItem()
        self.assertEqual (tree.GetChildrenCount (newrootitem2, True), 2)
        self.assertEqual (tree.GetChildrenCount (newrootitem2, False), 1)


    def testSelectedPage (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]

        selItem = tree.GetSelection()
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot.selectedPage)
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 1"])

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        selItem = tree.GetSelection()
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot.selectedPage)
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 2/Страница 3"])


    def testOrder1 (self):
        tree = self._getTreeCtrl()

        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        self.wikiroot[u"Страница 2"].order -= 1

        rootitem = tree.GetRootItem()
        page2Item, cookie = tree.GetFirstChild (rootitem)

        self.assertEqual (tree.GetChildrenCount (page2Item, False), 1)
        self.assertEqual (tree.GetChildrenCount (page2Item, True), 1)
        self.assertEqual (tree.GetItemData(page2Item), self.wikiroot[u"Страница 2"])
        self.assertEqual (tree.GetItemText (page2Item), u"Страница 2")

        page3Item, cookie = tree.GetFirstChild (page2Item)

        self.assertEqual (tree.GetChildrenCount (page3Item, True), 0)
        self.assertEqual (tree.GetChildrenCount (page3Item, False), 0)
        self.assertEqual (tree.GetItemData(page3Item), self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (tree.GetItemText (page3Item), u"Страница 3")


    def testOrder2 (self):
        tree = self._getTreeCtrl()

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.wikiroot[u"Страница 2"]

        selItem = tree.GetSelection()
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 2"])
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 2"])
        self.assertEqual (self.wikiroot.selectedPage, self.wikiroot[u"Страница 2"])

        Application.wikiroot.selectedPage.order -= 1

        selItem = tree.GetSelection()
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 2"])
        self.assertEqual (tree.GetItemData(selItem), self.wikiroot[u"Страница 2"])
        self.assertEqual (self.wikiroot.selectedPage, self.wikiroot[u"Страница 2"])

        rootitem = tree.GetRootItem()
        page2Item, cookie = tree.GetFirstChild (rootitem)

        self.assertEqual (tree.GetChildrenCount (page2Item, False), 1)
        self.assertEqual (tree.GetChildrenCount (page2Item, True), 1)
        self.assertEqual (tree.GetItemData(page2Item), self.wikiroot[u"Страница 2"])
        self.assertEqual (tree.GetItemText (page2Item), u"Страница 2")

        page3Item, cookie = tree.GetFirstChild (page2Item)

        self.assertEqual (tree.GetChildrenCount (page3Item, False), 0)
        self.assertEqual (tree.GetChildrenCount (page3Item, True), 0)
        self.assertEqual (tree.GetItemData(page3Item), self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (tree.GetItemText (page3Item), u"Страница 3")


    def testRename (self):
        tree = self._getTreeCtrl()
        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        self.wikiroot[u"Страница 2"].title = u"Переименованная страница"

        rootitem = tree.GetRootItem()
        firstItem, cookie = tree.GetFirstChild (rootitem)
        newPageItem = tree.GetNextSibling (firstItem)

        self.assertEqual (tree.GetChildrenCount (newPageItem, False), 1)
        self.assertEqual (tree.GetChildrenCount (newPageItem, True), 1)
        self.assertEqual (tree.GetItemData(newPageItem), self.wikiroot[u"Переименованная страница"])
        self.assertEqual (tree.GetItemText (newPageItem), u"Переименованная страница")

    def testInvalidIcon (self):
        tree = self._getTreeCtrl()
        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        page = factory.create (self.wikiroot, u"Страница 1", [])
        icon_name = u'../test/images/invalid.png'
        assert os.path.exists(icon_name)

        page.icon = icon_name

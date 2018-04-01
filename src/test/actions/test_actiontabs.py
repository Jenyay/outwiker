# -*- coding: utf-8 -*-

import unittest

from outwiker.actions.tabs import AddTabAction, CloseTabAction, PreviousTabAction, NextTabAction
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class ActionTabsTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self._tabsController = self.application.mainWindow.tabsController
        self._actionController = self.application.actionController

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testCloneEmpty2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        self._actionController.getAction(AddTabAction.stringId).run(None)

        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getPage(0), None)
        self.assertEqual(self._tabsController.getPage(1), None)

    def testCloneTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self._actionController.getAction(AddTabAction.stringId).run(None)
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 1")

        self._actionController.getAction(AddTabAction.stringId).run(None)
        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getSelection(), 2)

    def testCloneTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self._actionController.getAction(AddTabAction.stringId).run(None)
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self._actionController.getAction(AddTabAction.stringId).run(None)

        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 2")

        self.assertEqual(self._tabsController.getPage(2),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getTabTitle(2), "Страница 4")

    def testCloseLastTab(self):
        """
        Тест на попытку закрыть единственную вкладку
        """
        self.application.wikiroot = self.wikiroot
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        self._actionController.getAction(CloseTabAction.stringId).run(None)
        self.assertEqual(self._tabsController.getTabsCount(), 1)

    def testCloseTab(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertEqual(self._tabsController.getTabsCount(), 3)

        self._actionController.getAction(CloseTabAction.stringId).run(None)

        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])

        self._actionController.getAction(CloseTabAction.stringId).run(None)
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

        self._actionController.getAction(CloseTabAction.stringId).run(None)
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

    def testNextTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._actionController.getAction(NextTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getSelection(), 1)

        self._actionController.getAction(NextTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getSelection(), 2)

        self._actionController.getAction(NextTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testNextTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._actionController.getAction(NextTabAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testPrevTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._actionController.getAction(PreviousTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getSelection(), 2)

        self._actionController.getAction(PreviousTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getSelection(), 1)

        self._actionController.getAction(PreviousTabAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testPrevTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._actionController.getAction(PreviousTabAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testInvalidWiki(self):
        self.application.wikiroot = None

        self.assertRaises(AssertionError,
                          self._tabsController.openInTab,
                          self.wikiroot["Страница 2/Страница 3"],
                          False)

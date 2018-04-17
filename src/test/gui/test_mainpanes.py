# -*- coding: utf-8 -*-

import unittest

import wx.aui

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction
from test.basetestcases import BaseOutWikerGUIMixin


class MainPanesTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

        self.attachAction = self.application.actionController.getAction(ShowHideAttachesAction.stringId)
        self.treeAction = self.application.actionController.getAction(ShowHideTreeAction.stringId)
        self.tagsAction = self.application.actionController.getAction(ShowHideTagsAction.stringId)

    def tearDown(self):
        self.destroyApplication()

    def testPanesExists(self):
        self.assertNotEqual(self.mainWindow.treePanel, None)
        self.assertNotEqual(self.mainWindow.attachPanel, None)
        self.assertNotEqual(self.mainWindow.tagsCloudPanel, None)

    def testVisiblePanels(self):
        self.assertTrue(self.mainWindow.treePanel.isShown())
        self.assertTrue(self.mainWindow.attachPanel.isShown())
        self.assertTrue(self.mainWindow.tagsCloudPanel.isShown())

    def testMenuCheck(self):
        self._testMenuCheckForAction(self.treeAction)
        self._testMenuCheckForAction(self.attachAction)
        self._testMenuCheckForAction(self.tagsAction)

    def testClose(self):
        self._testClose(self.treeAction, self.mainWindow.treePanel)
        self._testClose(self.attachAction, self.mainWindow.attachPanel)
        self._testClose(self.tagsAction, self.mainWindow.tagsCloudPanel)

    def _testClose(self, action, panel):
        actionInfo = self.application.actionController.getActionInfo(action.stringId)

        self.assertTrue(actionInfo.menuItem.IsChecked())

        # Небольшой хак с генерацией события о закрытии панели
        event = wx.aui.AuiManagerEvent(wx.aui.wxEVT_AUI_PANE_CLOSE)
        event.SetPane(panel.pane)
        self.mainWindow.auiManager.ProcessEvent(event)

        self.assertFalse(actionInfo.menuItem.IsChecked())
        self.assertFalse(panel.isShown())

        self.application.actionController.check(action.stringId, True)

        self.assertTrue(actionInfo.menuItem.IsChecked())
        self.assertTrue(panel.isShown())

    def _testMenuCheckForAction(self, action):
        actionInfo = self.application.actionController.getActionInfo(action.stringId)

        self.assertNotEqual(actionInfo.menuItem, None)

        self.assertTrue(actionInfo.menuItem.IsCheckable())
        self.assertTrue(actionInfo.menuItem.IsChecked())

        self.application.actionController.check(action.stringId, False)
        self.assertFalse(actionInfo.menuItem.IsChecked())

        self.application.actionController.check(action.stringId, True)
        self.assertTrue(actionInfo.menuItem.IsChecked())

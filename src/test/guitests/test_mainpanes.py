# -*- coding: UTF-8 -*-

import wx.aui

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction

from outwiker.core.application import Application
from .basemainwnd import BaseMainWndTest


class MainPanesTest (BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.attachAction = Application.actionController.getAction (ShowHideAttachesAction.stringId)
        self.treeAction = Application.actionController.getAction (ShowHideTreeAction.stringId)
        self.tagsAction = Application.actionController.getAction (ShowHideTagsAction.stringId)


    def testPanesExists (self):
        self.assertNotEqual (self.wnd.treePanel, None)
        self.assertNotEqual (self.wnd.attachPanel, None)
        self.assertNotEqual (self.wnd.tagsCloudPanel, None)


    def testVisiblePanels (self):
        self.assertTrue (self.wnd.treePanel.isShown())
        self.assertTrue (self.wnd.attachPanel.isShown())
        self.assertTrue (self.wnd.tagsCloudPanel.isShown())


    def testMenuCheck (self):
        self._testMenuCheckForAction (self.treeAction)
        self._testMenuCheckForAction (self.attachAction)
        self._testMenuCheckForAction (self.tagsAction)


    def testClose (self):
        self._testClose (self.treeAction, self.wnd.treePanel)
        self._testClose (self.attachAction, self.wnd.attachPanel)
        self._testClose (self.tagsAction, self.wnd.tagsCloudPanel)


    def _testClose (self, action, panel):
        actionInfo = Application.actionController.getActionInfo (action.stringId)

        self.assertTrue (actionInfo.menuItem.IsChecked())

        # Небольшой хак с генерацией события о закрытии панели
        event = wx.aui.AuiManagerEvent (wx.aui.wxEVT_AUI_PANE_CLOSE)
        event.SetPane(panel.pane)
        self.wnd.auiManager.ProcessEvent (event)

        self.assertFalse (actionInfo.menuItem.IsChecked())
        self.assertFalse (panel.isShown())

        Application.actionController.check (action.stringId, True)

        self.assertTrue (actionInfo.menuItem.IsChecked())
        self.assertTrue (panel.isShown())


    def _testMenuCheckForAction (self, action):
        actionInfo = Application.actionController.getActionInfo (action.stringId)

        self.assertNotEqual (actionInfo.menuItem, None)

        self.assertTrue (actionInfo.menuItem.IsCheckable())
        self.assertTrue (actionInfo.menuItem.IsChecked())

        Application.actionController.check (action.stringId, False)
        self.assertFalse (actionInfo.menuItem.IsChecked())

        Application.actionController.check (action.stringId, True)
        self.assertTrue (actionInfo.menuItem.IsChecked())

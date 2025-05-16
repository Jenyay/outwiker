# -*- coding: utf-8 -*-

import unittest

from outwiker.app.actions.showhidetree import ShowHideTreeAction
from outwiker.app.actions.showhideattaches import ShowHideAttachesAction
from outwiker.app.actions.showhidetags import ShowHideTagsAction
from outwiker.app.actions.fullscreen import FullScreenAction
from outwiker.core.system import getOS
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class FullScreenTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication(enableActionsGui=True, createTreePanel=True, createAttachPanel=True, createTagsPanel=True)

    def testFullScreenStart(self):
        fullScreenActionInfo = self.application.actionController.getActionInfo(
            FullScreenAction.stringId)

        if getOS().name == 'windows':
            self.assertFalse(self.mainWindow.IsFullScreen())

        self.assertFalse(fullScreenActionInfo.menuItem.IsChecked())
        self.assertTrue(self.mainWindow.treePanel.isShown())
        self.assertTrue(self.mainWindow.attachPanel.isShown())
        self.assertTrue(self.mainWindow.tagsCloudPanel.isShown())

    def tearDown(self):
        self.destroyApplication()

    def testFullScreen(self):
        showHideTreeActionInfo = self.application.actionController.getActionInfo(
            ShowHideTreeAction.stringId)
        showHideAttachesActionInfo = self.application.actionController.getActionInfo(
            ShowHideAttachesAction.stringId)
        showHideTagsActionInfo = self.application.actionController.getActionInfo(
            ShowHideTagsAction.stringId)

        self.application.actionController.check(FullScreenAction.stringId, True)

        if getOS().name == 'windows':
            self.assertTrue(self.mainWindow.IsFullScreen())

        self.assertFalse(self.mainWindow.treePanel.isShown())
        self.assertFalse(self.mainWindow.attachPanel.isShown())
        self.assertFalse(self.mainWindow.tagsCloudPanel.isShown())

        self.assertFalse(showHideTreeActionInfo.menuItem.IsChecked())
        self.assertFalse(showHideAttachesActionInfo.menuItem.IsChecked())
        self.assertFalse(showHideTagsActionInfo.menuItem.IsChecked())

        self.application.actionController.check(FullScreenAction.stringId, False)

        if getOS().name == 'windows':
            self.assertFalse(self.mainWindow.IsFullScreen())

        self.assertTrue(self.mainWindow.treePanel.isShown())
        self.assertTrue(self.mainWindow.attachPanel.isShown())
        self.assertTrue(self.mainWindow.tagsCloudPanel.isShown())

        self.assertTrue(showHideTreeActionInfo.menuItem.IsChecked())
        self.assertTrue(showHideAttachesActionInfo.menuItem.IsChecked())
        self.assertTrue(showHideTagsActionInfo.menuItem.IsChecked())

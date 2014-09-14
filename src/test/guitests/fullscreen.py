# -*- coding: UTF-8 -*-

from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetags import ShowHideTagsAction
from outwiker.actions.fullscreen import FullScreenAction

from outwiker.core.application import Application
from basemainwnd import BaseMainWndTest


class FullScreenTest (BaseMainWndTest):
    def testFullScreenStart (self):
        fullScreenActionInfo = Application.actionController.getActionInfo (FullScreenAction.stringId)

        self.assertFalse (self.wnd.IsFullScreen())
        self.assertFalse (fullScreenActionInfo.menuItem.IsChecked())
        self.assertTrue (self.wnd.treePanel.isShown())
        self.assertTrue (self.wnd.attachPanel.isShown())
        self.assertTrue (self.wnd.tagsCloudPanel.isShown())


    def testFullScreen (self):
        showHideTreeActionInfo = Application.actionController.getActionInfo (ShowHideTreeAction.stringId)
        showHideAttachesActionInfo = Application.actionController.getActionInfo (ShowHideAttachesAction.stringId)
        showHideTagsActionInfo = Application.actionController.getActionInfo (ShowHideTagsAction.stringId)

        Application.actionController.check (FullScreenAction.stringId, True)

        self.assertTrue (self.wnd.IsFullScreen())
        self.assertFalse (self.wnd.treePanel.isShown())
        self.assertFalse (self.wnd.attachPanel.isShown())
        self.assertFalse (self.wnd.tagsCloudPanel.isShown())

        self.assertFalse (showHideTreeActionInfo.menuItem.IsChecked())
        self.assertFalse (showHideAttachesActionInfo.menuItem.IsChecked())
        self.assertFalse (showHideTagsActionInfo.menuItem.IsChecked())

        Application.actionController.check (FullScreenAction.stringId, False)

        self.assertFalse (self.wnd.IsFullScreen())
        self.assertTrue (self.wnd.treePanel.isShown())
        self.assertTrue (self.wnd.attachPanel.isShown())
        self.assertTrue (self.wnd.tagsCloudPanel.isShown())

        self.assertTrue (showHideTreeActionInfo.menuItem.IsChecked())
        self.assertTrue (showHideAttachesActionInfo.menuItem.IsChecked())
        self.assertTrue (showHideTagsActionInfo.menuItem.IsChecked())

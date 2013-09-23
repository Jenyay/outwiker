#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction

from outwiker.gui.wxactioncontroller import WxActionController
from outwiker.core.application import Application
from basemainwnd import BaseMainWndTest


class MainPanesTest (BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self.actionController = WxActionController(self.wnd)

        # self.wnd.createGui()


    def testPanesExists (self):
        self.assertNotEqual (self.wnd.treePanel, None)
        self.assertNotEqual (self.wnd.attachPanel, None)
        self.assertNotEqual (self.wnd.tagsCloudPanel, None)

# -*- coding: UTF-8 -*-

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application


class DescriptionActionTest (BaseMainWndTest):
    """
    Tests for search empty title and description of actions
    """
    def testDescriptions (self):
        for stringId in Application.actionController.getActionsStrId():
            action = Application.actionController.getAction (stringId)
            self.assertNotEqual (len (action.title), 0, type (action))
            self.assertNotEqual (len (action.description), 0, type (action))

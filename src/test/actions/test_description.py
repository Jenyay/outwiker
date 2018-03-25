# -*- coding: utf-8 -*-

from test.basetestcases import BaseOutWikerGUITest


class DescriptionActionTest (BaseOutWikerGUITest):
    """
    Tests for search empty title and description of actions
    """
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def testDescriptions(self):
        for stringId in self.application.actionController.getActionsStrId():
            action = self.application.actionController.getAction(stringId)
            self.assertNotEqual(len(action.title), 0, type(action))
            self.assertNotEqual(len(action.description), 0, type(action))

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.gui.wxactioncontroller import WxActionController
from outwiker.gui.baseaction import BaseAction
from outwiker.core.application import Application
from basemainwnd import BaseMainWndTest


class TestAction (BaseAction):
    def __init__ (self):
        self.runCount = 0


    @property
    def title (self):
        return u"Тестовый Action"


    @property
    def strid (self):
        return u"test_action"
    
    
    def run (self):
        self.runCount += 1


class ActionControllerTest (BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self.actionController = WxActionController(self.wnd)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)


    def testAppendAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.appendAction (action, menu)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.appendAction (action, menu)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeAction (action.strid)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)



    def testRunAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.appendAction (action, menu)
        self._emulateMenuClick (action, menu)

        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.strid)

        # Убедимся, что после удаления пункта меню, событие больше не срабатывает
        self._emulateMenuClick (action, menu)
        self.assertEqual (action.runCount, 1)


    def _emulateMenuClick (self, action, menu):
        """
        Эмуляция события выбора пункта меню
        """
        item_id = menu.FindItem (action.title)
        event = wx.CommandEvent (wx.wxEVT_COMMAND_MENU_SELECTED, item_id)
        self.wnd.ProcessEvent (event)

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


    def testRegisterAction (self):
        action = TestAction()

        self.assertEqual (len (self.actionController.actions), 0)

        self.actionController.register (action)

        self.assertEqual (len (self.actionController.actions), 1)


    def testAppendMenu (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (len (self.actionController.actions), 1)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)
        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.strid)

        self.assertEqual (len (self.actionController.actions), 0)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)
        self.assertEqual (toolbar.GetToolCount(), 0)


    def testRemoveActionAndRun (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        menuItemId = self._getMenuItemId (action.strid)
        toolItemId = self._getToolItemId (action.strid)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 2)

        self.actionController.removeAction (action.strid)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 2)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 2)


    def testRunAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        
        menuItemId = self._getMenuItemId (action.strid)

        self._emulateMenuClick (menuItemId)

        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.strid)

        # Убедимся, что после удаления пункта меню, событие больше не срабатывает
        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)


    def testAppendToolbarButton (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 0)



    def testAppendToolbarButtonOnly (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 0)


    def testAppendToolbarButtonAndRun (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        menuItemId = self._getMenuItemId (action.strid)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.strid)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)


    def testAppendToolbarButtonOnlyAndRun (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        toolItemId = self._getToolItemId (action.strid)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.strid)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)


    def testRemoveToolButton (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeToolbarButton (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveToolButtonInvalid (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeToolbarButton (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveMenuItemInvalid (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeMenuItem (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveMenuItem (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.strid, menu)
        self.actionController.appendToolbarButton (action.strid, 
                toolbar,
                image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertNotEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeMenuItem (action.strid)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def _emulateMenuClick (self, menuItemId):
        """
        Эмуляция события выбора пункта меню
        """
        event = wx.CommandEvent (wx.wxEVT_COMMAND_MENU_SELECTED, menuItemId)
        self.wnd.ProcessEvent (event)


    def _emulateButtonClick (self, toolitemId):
        """
        Эмуляция события выбора пункта меню
        """
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        event = wx.CommandEvent (wx.wxEVT_COMMAND_TOOL_CLICKED, toolitemId)
        self.wnd.ProcessEvent (event)


    def _getMenuItemId (self, strid):
        result = None
        for actionInfo in self.actionController.actions:
            if actionInfo.action.strid == strid:
                result = actionInfo.menuItem.GetId()
                break

        return result


    def _getToolItemId (self, strid):
        """
        Получить идентификатор кнопки с панели инструментов
        """
        result = None
        for actionInfo in self.actionController.actions:
            if actionInfo.action.strid == strid:
                result = actionInfo.toolItemId
                break

        return result

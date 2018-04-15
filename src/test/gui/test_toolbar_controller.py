# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.controls.toolbar2 import ToolBar2Container
from outwiker.gui.toolbarscontroller import ToolBarsController
from test.basetestcases import BaseOutWikerMixin


class ToolBarsControllerTest(unittest.TestCase, BaseOutWikerMixin):
    def setUp(self):
        self.initApplication()
        self._wxapp = wx.App()
        self.mainWindow = wx.Frame(None)
        self._wxapp.SetTopWindow(self.mainWindow)

        self.parentMenu = wx.Menu()
        self.toolbar_container = ToolBar2Container(self.mainWindow)
        self.controller = ToolBarsController(
            self.parentMenu,
            self.toolbar_container,
            self.application.config)

    def tearDown(self):
        self.controller.destroyAllToolBars()
        self.mainWindow.Close()
        self._wxapp.MainLoop()
        del self._wxapp
        self.destroyApplication()

    def test_create_controller(self):
        pass

    def test_create_single_toolbar(self):
        toolbar_id = u'Абырвалг ID'
        toolbar_title = 'Абырвалг'

        self.controller.createToolBar(toolbar_id, toolbar_title)
        menu_item = self.controller.getMenuItem(toolbar_id)

        self.assertIsNotNone(menu_item)
        self.assertEqual(menu_item.GetText(), toolbar_title)
        self.assertTrue(menu_item.IsChecked())
        self.assertTrue(self.toolbar_container[toolbar_id].IsShown())

    def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
        """
        Since the tests are usually run before MainLoop is called then we
        need to make our own EventLoop for Yield to actually do anything
        useful.

        The method taken from wxPython tests.
        """
        evtLoop = self._wxapp.GetTraits().CreateEventLoop()
        activator = wx.EventLoopActivator(evtLoop)
        evtLoop.YieldFor(eventsToProcess)

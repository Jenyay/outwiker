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

    def test_order_01(self):
        toolbar_id_1 = u'Абырвалг ID 01'
        toolbar_title_1 = 'Абырвалг 01'
        toolbar_order_1 = 10

        self.controller.createToolBar(toolbar_id_1,
                                      toolbar_title_1,
                                      toolbar_order_1)
        menu_item_1 = self.controller.getMenuItem(toolbar_id_1)

        toolbar_id_2 = u'Абырвалг ID 02'
        toolbar_title_2 = 'Абырвалг 02'
        toolbar_order_2 = 10

        self.controller.createToolBar(toolbar_id_2,
                                      toolbar_title_2,
                                      toolbar_order_2)
        menu_item_2 = self.controller.getMenuItem(toolbar_id_2)

        menu_items = self.controller.getMenu().GetMenuItems()

        self.assertEqual(menu_item_1.GetId(), menu_items[0].GetId())
        self.assertEqual(menu_item_2.GetId(), menu_items[1].GetId())

    def test_order_02(self):
        toolbar_id_1 = u'Абырвалг ID 01'
        toolbar_title_1 = 'Абырвалг 01'
        toolbar_order_1 = 10

        self.controller.createToolBar(toolbar_id_1,
                                      toolbar_title_1,
                                      toolbar_order_1)
        menu_item_1 = self.controller.getMenuItem(toolbar_id_1)

        toolbar_id_2 = u'Абырвалг ID 02'
        toolbar_title_2 = 'Абырвалг 02'
        toolbar_order_2 = 20

        self.controller.createToolBar(toolbar_id_2,
                                      toolbar_title_2,
                                      toolbar_order_2)
        menu_item_2 = self.controller.getMenuItem(toolbar_id_2)

        menu_items = self.controller.getMenu().GetMenuItems()

        self.assertEqual(menu_item_1.GetId(), menu_items[0].GetId())
        self.assertEqual(menu_item_2.GetId(), menu_items[1].GetId())

    def test_order_03(self):
        toolbar_id_1 = u'Абырвалг ID 01'
        toolbar_title_1 = 'Абырвалг 01'
        toolbar_order_1 = 10

        self.controller.createToolBar(toolbar_id_1,
                                      toolbar_title_1,
                                      toolbar_order_1)
        menu_item_1 = self.controller.getMenuItem(toolbar_id_1)

        toolbar_id_2 = u'Абырвалг ID 02'
        toolbar_title_2 = 'Абырвалг 02'
        toolbar_order_2 = 5
        # from pudb import set_trace; set_trace()

        self.controller.createToolBar(toolbar_id_2,
                                      toolbar_title_2,
                                      toolbar_order_2)
        menu_item_2 = self.controller.getMenuItem(toolbar_id_2)

        menu_items = self.controller.getMenu().GetMenuItems()

        self.assertEqual(menu_item_1.GetId(), menu_items[1].GetId())
        self.assertEqual(menu_item_2.GetId(), menu_items[0].GetId())

    def test_order_04(self):
        toolbar_id_1 = u'Абырвалг ID 01'
        toolbar_title_1 = 'Абырвалг 01'
        toolbar_order_1 = 10

        self.controller.createToolBar(toolbar_id_1,
                                      toolbar_title_1,
                                      toolbar_order_1)
        menu_item_1 = self.controller.getMenuItem(toolbar_id_1)

        toolbar_id_2 = u'Абырвалг ID 02'
        toolbar_title_2 = 'Абырвалг 02'
        toolbar_order_2 = 20

        self.controller.createToolBar(toolbar_id_2,
                                      toolbar_title_2,
                                      toolbar_order_2)
        menu_item_2 = self.controller.getMenuItem(toolbar_id_2)

        toolbar_id_3 = u'Абырвалг ID 03'
        toolbar_title_3 = 'Абырвалг 03'
        toolbar_order_3 = 15

        self.controller.createToolBar(toolbar_id_3,
                                      toolbar_title_3,
                                      toolbar_order_3)
        menu_item_3 = self.controller.getMenuItem(toolbar_id_3)

        menu_items = self.controller.getMenu().GetMenuItems()

        self.assertEqual(menu_item_1.GetId(), menu_items[0].GetId())
        self.assertEqual(menu_item_3.GetId(), menu_items[1].GetId())
        self.assertEqual(menu_item_2.GetId(), menu_items[2].GetId())

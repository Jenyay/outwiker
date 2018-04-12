# -*- coding: utf-8 -*-

import wx

from test.basetestcases import BaseWxTestCase
from outwiker.gui.controls.toolbar2 import ToolBar2Container


class TestToolbar2(BaseWxTestCase):
    def setUp(self):
        super().setUp()
        self.initMainWindow()
        self.toolbarContainer = ToolBar2Container(self.mainWindow)

    def test_init(self):
        self.assertEqual(len(self.toolbarContainer), 0)

    def test_create_toolbar(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        self.assertEqual(len(self.toolbarContainer), 1)
        self.assertEqual(toolbar, self.toolbarContainer[toolbar_id])
        self.assertEqual(toolbar.GetToolsCount(), 0)
        self.assertEqual(len(toolbar), 0)

    def test_destroy_toolbar(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        self.assertEqual(len(self.toolbarContainer), 1)
        self.assertEqual(toolbar, self.toolbarContainer[toolbar_id])
        self.assertEqual(toolbar.GetToolsCount(), 0)
        self.assertEqual(len(toolbar), 0)

        self.toolbarContainer.destroyToolBar(toolbar_id)
        self.assertEqual(len(self.toolbarContainer), 0)

    def test_toolbar_create_button_from_image(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = '../test/images/16x16.png'
        tool_id = toolbar.AddButton(label, bitmap)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(len(toolbar), 1)
        self.assertIsNotNone(toolbar[tool_id])
        self.assertIsNotNone(toolbar.FindById(tool_id))
        self.assertEqual(toolbar[tool_id].GetKind(), wx.ITEM_NORMAL)

    def test_toolbar_create_button_from_bitmap(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        tool_id = toolbar.AddButton(label, bitmap)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(len(toolbar), 1)
        self.assertIsNotNone(toolbar[tool_id])
        self.assertIsNotNone(toolbar.FindById(tool_id))
        self.assertEqual(toolbar[tool_id].GetKind(), wx.ITEM_NORMAL)

    def test_toolbar_add_separator(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        toolbar.AddSeparator()
        self.assertEqual(len(toolbar), 1)

    def test_toolbar_create_checkbutton_from_image(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = '../test/images/16x16.png'
        tool_id = toolbar.AddCheckButton(label, bitmap)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(len(toolbar), 1)
        self.assertIsNotNone(toolbar[tool_id])
        self.assertIsNotNone(toolbar.FindById(tool_id))
        self.assertEqual(toolbar[tool_id].GetKind(), wx.ITEM_CHECK)

    def test_toolbar_create_checkbutton_from_bitmap(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        tool_id = toolbar.AddCheckButton(label, bitmap)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(len(toolbar), 1)
        self.assertIsNotNone(toolbar[tool_id])
        self.assertIsNotNone(toolbar.FindById(tool_id))
        self.assertEqual(toolbar[tool_id].GetKind(), wx.ITEM_CHECK)

    def test_toolbar_delete_tool(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        tool_id = toolbar.AddButton(label, bitmap)
        toolbar.Realize()

        self.assertEqual(len(toolbar), 1)

        toolbar.DeleteTool(tool_id)
        toolbar.Realize()

        self.assertEqual(len(toolbar), 0)

    def test_toolbar_checkbutton(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        tool_id = toolbar.AddCheckButton(label, bitmap)
        toolbar.Realize()

        self.assertFalse(toolbar.IsChecked(tool_id))

        toolbar.ToggleTool(tool_id, True)
        toolbar.Realize()

        self.assertTrue(toolbar.IsChecked(tool_id))

        toolbar.ToggleTool(tool_id, False)
        toolbar.Realize()

        self.assertFalse(toolbar.IsChecked(tool_id))

    def test_toolbar_enabled(self):
        toolbar_id = 'Панель инструментов 1'
        toolbar = self.toolbarContainer.createToolBar(toolbar_id)

        label = 'Инструмент 1'
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
        tool_id = toolbar.AddButton(label, bitmap)
        toolbar.Realize()

        toolbar.EnableTool(tool_id, False)
        toolbar.Realize()

        self.assertFalse(toolbar.GetToolEnabled(tool_id))

        toolbar.EnableTool(tool_id, True)
        toolbar.Realize()

        self.assertTrue(toolbar.GetToolEnabled(tool_id))

    def test_toolbar_order_01(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 10
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 20
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        self.assertEqual(toolbar_1.GetOrder(), toolbar_1_order)
        self.assertEqual(toolbar_2.GetOrder(), toolbar_2_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_1)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_2)

    def test_toolbar_order_02(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 20
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 10
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_2)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_1)

    def test_toolbar_order_03(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 10
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 10
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_1)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_2)

    def test_toolbar_order_04(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 10
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 20
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        toolbar_3_id = 'Панель инструментов 3'
        toolbar_3_order = 0
        toolbar_3 = self.toolbarContainer.createToolBar(toolbar_3_id,
                                                        order=toolbar_3_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_3)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_1)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(2), toolbar_2)

    def test_toolbar_order_05(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 20
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 10
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        toolbar_3_id = 'Панель инструментов 3'
        toolbar_3_order = 0
        toolbar_3 = self.toolbarContainer.createToolBar(toolbar_3_id,
                                                        order=toolbar_3_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_3)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_2)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(2), toolbar_1)

    def test_toolbar_order_06(self):
        toolbar_1_id = 'Панель инструментов 1'
        toolbar_1_order = 20
        toolbar_1 = self.toolbarContainer.createToolBar(toolbar_1_id,
                                                        order=toolbar_1_order)

        toolbar_2_id = 'Панель инструментов 2'
        toolbar_2_order = 10
        toolbar_2 = self.toolbarContainer.createToolBar(toolbar_2_id,
                                                        order=toolbar_2_order)

        toolbar_3_id = 'Панель инструментов 3'
        toolbar_3_order = 0
        toolbar_3 = self.toolbarContainer.createToolBar(toolbar_3_id,
                                                        order=toolbar_3_order)

        toolbar_4_id = 'Панель инструментов 4'
        toolbar_4_order = 0
        toolbar_4 = self.toolbarContainer.createToolBar(toolbar_4_id,
                                                        order=toolbar_4_order)

        self.assertEqual(self.toolbarContainer.getToolBarByIndex(0), toolbar_3)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(1), toolbar_4)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(2), toolbar_2)
        self.assertEqual(self.toolbarContainer.getToolBarByIndex(3), toolbar_1)

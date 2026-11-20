# -*- coding: utf-8 -*-

import pytest
import wx

from outwiker.gui.controls.toolbar2 import ToolBar2Container

TOOLBAR_ID = "Панель инструментов 1"
TOOL_LABEL = "Инструмент 1"
IMAGE_PATH = "testdata/images/16x16.png"


@pytest.fixture
def toolbar_container(empty_window: wx.Frame) -> ToolBar2Container:
    """Replaces the setUp() method of the former TestToolbar2 class."""
    return ToolBar2Container(empty_window)


def test_init(toolbar_container: ToolBar2Container):
    assert len(toolbar_container) == 0


def test_create_toolbar(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    assert len(toolbar_container) == 1
    assert toolbar == toolbar_container[TOOLBAR_ID]
    assert toolbar.GetToolsCount() == 0
    assert len(toolbar) == 0


def test_destroy_toolbar(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    assert len(toolbar_container) == 1
    assert toolbar == toolbar_container[TOOLBAR_ID]
    assert toolbar.GetToolsCount() == 0
    assert len(toolbar) == 0

    toolbar_container.destroyToolBar(TOOLBAR_ID)
    assert len(toolbar_container) == 0


def test_toolbar_create_button_from_image(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    tool_id = toolbar.AddButton(TOOL_LABEL, IMAGE_PATH)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert len(toolbar) == 1
    assert toolbar[tool_id] is not None
    assert toolbar.FindById(tool_id) is not None
    assert toolbar[tool_id].GetKind() == wx.ITEM_NORMAL


def test_toolbar_create_button_from_bitmap(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
    tool_id = toolbar.AddButton(TOOL_LABEL, bitmap)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert len(toolbar) == 1
    assert toolbar[tool_id] is not None
    assert toolbar.FindById(tool_id) is not None
    assert toolbar[tool_id].GetKind() == wx.ITEM_NORMAL


def test_toolbar_add_separator(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    toolbar.AddSeparator()
    assert len(toolbar) == 1


def test_toolbar_create_checkbutton_from_image(
    toolbar_container: ToolBar2Container,
):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    tool_id = toolbar.AddCheckButton(TOOL_LABEL, IMAGE_PATH)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert len(toolbar) == 1
    assert toolbar[tool_id] is not None
    assert toolbar.FindById(tool_id) is not None
    assert toolbar[tool_id].GetKind() == wx.ITEM_CHECK


def test_toolbar_create_checkbutton_from_bitmap(
    toolbar_container: ToolBar2Container,
):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
    tool_id = toolbar.AddCheckButton(TOOL_LABEL, bitmap)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert len(toolbar) == 1
    assert toolbar[tool_id] is not None
    assert toolbar.FindById(tool_id) is not None
    assert toolbar[tool_id].GetKind() == wx.ITEM_CHECK


def test_toolbar_delete_tool(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
    tool_id = toolbar.AddButton(TOOL_LABEL, bitmap)
    toolbar.Realize()

    assert len(toolbar) == 1

    toolbar.DeleteTool(tool_id)
    toolbar.Realize()

    assert len(toolbar) == 0


def test_toolbar_checkbutton(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
    tool_id = toolbar.AddCheckButton(TOOL_LABEL, bitmap)
    toolbar.Realize()

    assert not toolbar.IsChecked(tool_id)

    toolbar.ToggleTool(tool_id, True)
    toolbar.Realize()

    assert toolbar.IsChecked(tool_id)

    toolbar.ToggleTool(tool_id, False)
    toolbar.Realize()

    assert not toolbar.IsChecked(tool_id)


def test_toolbar_enabled(toolbar_container: ToolBar2Container):
    toolbar = toolbar_container.createToolBar(TOOLBAR_ID)

    bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
    tool_id = toolbar.AddButton(TOOL_LABEL, bitmap)
    toolbar.Realize()

    toolbar.EnableTool(tool_id, False)
    toolbar.Realize()

    assert not toolbar.GetToolEnabled(tool_id)

    toolbar.EnableTool(tool_id, True)
    toolbar.Realize()

    assert toolbar.GetToolEnabled(tool_id)


def test_toolbar_order_01(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 10
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 20
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    assert toolbar_1.GetOrder() == toolbar_1_order
    assert toolbar_2.GetOrder() == toolbar_2_order

    assert toolbar_container.getToolBarByIndex(0) == toolbar_1
    assert toolbar_container.getToolBarByIndex(1) == toolbar_2


def test_toolbar_order_02(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 20
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 10
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    assert toolbar_container.getToolBarByIndex(0) == toolbar_2
    assert toolbar_container.getToolBarByIndex(1) == toolbar_1


def test_toolbar_order_03(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 10
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 10
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    assert toolbar_container.getToolBarByIndex(0) == toolbar_1
    assert toolbar_container.getToolBarByIndex(1) == toolbar_2


def test_toolbar_order_04(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 10
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 20
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    toolbar_3_id = "Панель инструментов 3"
    toolbar_3_order = 0
    toolbar_3 = toolbar_container.createToolBar(toolbar_3_id, order=toolbar_3_order)

    assert toolbar_container.getToolBarByIndex(0) == toolbar_3
    assert toolbar_container.getToolBarByIndex(1) == toolbar_1
    assert toolbar_container.getToolBarByIndex(2) == toolbar_2


def test_toolbar_order_05(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 20
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 10
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    toolbar_3_id = "Панель инструментов 3"
    toolbar_3_order = 0
    toolbar_3 = toolbar_container.createToolBar(toolbar_3_id, order=toolbar_3_order)

    assert toolbar_container.getToolBarByIndex(0) == toolbar_3
    assert toolbar_container.getToolBarByIndex(1) == toolbar_2
    assert toolbar_container.getToolBarByIndex(2) == toolbar_1


def test_toolbar_order_06(toolbar_container: ToolBar2Container):
    toolbar_1_id = "Панель инструментов 1"
    toolbar_1_order = 20
    toolbar_1 = toolbar_container.createToolBar(toolbar_1_id, order=toolbar_1_order)

    toolbar_2_id = "Панель инструментов 2"
    toolbar_2_order = 10
    toolbar_2 = toolbar_container.createToolBar(toolbar_2_id, order=toolbar_2_order)

    toolbar_3_id = "Панель инструментов 3"
    toolbar_3_order = 0
    toolbar_3 = toolbar_container.createToolBar(toolbar_3_id, order=toolbar_3_order)

    toolbar_4_id = "Панель инструментов 4"
    toolbar_4_order = 0
    toolbar_4 = toolbar_container.createToolBar(toolbar_4_id, order=toolbar_4_order)

    assert toolbar_container.getToolBarByIndex(0) == toolbar_3
    assert toolbar_container.getToolBarByIndex(1) == toolbar_4
    assert toolbar_container.getToolBarByIndex(2) == toolbar_2
    assert toolbar_container.getToolBarByIndex(3) == toolbar_1

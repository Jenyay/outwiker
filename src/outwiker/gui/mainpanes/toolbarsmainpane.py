# -*- coding: utf-8 -*-

import wx.aui

from .mainpane import MainPane
from ..controls.toolbar2 import ToolBar2Container


class ToolBarsMainPane(MainPane):
    """
    Класс для работы с панелью с контентом страницы
    """
    def _createPanel(self):
        panel = ToolBar2Container(self.parent)
        return panel

    def _createConfig(self):
        return None

    @property
    def caption(self):
        return _(u"Toolbars")

    def _createPane(self):
        """
        Создать класс с информацией о панели для auiManager
        """
        pane = wx.aui.AuiPaneInfo().Name("ToolbarsPane").Gripper(False).CaptionVisible(False).Layer(2).Position(0).CloseButton(False).MaximizeButton(False).Top().Dock()

        return pane

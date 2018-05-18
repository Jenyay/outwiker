# -*- coding: utf-8 -*-

import wx.aui

from .mainpane import MainPane
from ..currentpagepanel import CurrentPagePanel


class PageMainPane(MainPane):
    """
    Класс для работы с панелью с контентом страницы
    """
    def _createPanel(self):
        return CurrentPagePanel(self.parent, self._application)

    def _createConfig(self):
        return None

    @property
    def caption(self):
        return _(u"Note")

    @property
    def pageView(self):
        return self.panel.pageView

    def _createPane(self):
        """
        Создать класс с информацией о панели для auiManager
        """
        pane = wx.aui.AuiPaneInfo().Name("pagePane").Gripper(False).CaptionVisible(False).Layer(0).Position(0).CloseButton(False).MaximizeButton(False).Center().Dock()

        return pane

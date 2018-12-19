# -*- coding: utf-8 -*-

import wx.aui

from .mainpane import MainPane
from ..tagscloudpanel import TagsCloudPanel
from ..guiconfig import TagsCloudConfig


class TagsCloudMainPane (MainPane):
    """
    Класс для работы с панелью с облаком тегов в главном окне
    """

    def _createPanel(self):
        return TagsCloudPanel(self.parent, self.application)

    def _createConfig(self):
        return TagsCloudConfig(self.application.config)

    def _createPane(self):
        """
        Создать класс с информацией о панели для auiManager
        """
        pane = self._loadPaneInfo(self.config.pane)

        if pane is None:
            pane = self._getPaneDefault()

        pane.Dock()
        pane.CloseButton()
        pane.Caption(self.caption)

        pane.BestSize((self.config.width.value,
                       self.config.height.value))

        return pane

    def _getPaneDefault(self):
        treepane = self._auiManager.GetPane(self._parent.GetParent().treePanel.panel)
        layer = treepane.dock_layer
        direction = treepane.dock_direction
        paneName = "TagsPane"

        pane = wx.aui.AuiPaneInfo().Name(paneName).Caption(self.caption).Gripper(False).CaptionVisible(True).Layer(layer).Position(1).CloseButton(True).MaximizeButton(False).Direction(direction).Dock()

        return pane

    @property
    def caption(self):
        return _(u"Tags")

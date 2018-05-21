# -*- coding: utf-8 -*-

import wx.aui

from .mainpane import MainPane
from ..guiconfig import AttachConfig
from ..attachpanel import AttachPanel


class AttachMainPane(MainPane):
    def _createPanel(self):
        return AttachPanel(self.parent, self.application)

    def _createConfig(self):
        return AttachConfig(self.application.config)

    @property
    def caption(self):
        return _(u"Attachments")

    def _createPane(self):
        pane = self._loadPaneInfo(self.config.pane)

        if pane is None:
            pane = self._getPaneDefault()

        pane.Dock()
        pane.CloseButton()
        pane.Caption(self.caption)

        return pane

    def _getPaneDefault(self):
        pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(self.caption).Gripper(False).CaptionVisible(True).Layer(0).Position(0).CloseButton(True).MaximizeButton(False).Bottom().Dock()

        return pane

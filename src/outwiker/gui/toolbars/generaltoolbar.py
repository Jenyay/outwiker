# -*- coding: UTF-8 -*-

import wx
import wx.aui

from .basetoolbar import BaseToolBar


class GeneralToolBar (BaseToolBar):
    def __init__(self, parent, auiManager):
        super(GeneralToolBar, self).__init__(parent, auiManager)

    def _createPane(self):
        return (wx.aui.AuiPaneInfo()
                .Name(self.name)
                .Caption(self.caption)
                .ToolbarPane()
                .Top()
                .Position(0)
                .Row(0))

    @property
    def name(self):
        return u"generalToolBar"

    @property
    def caption(self):
        return _(u"General")

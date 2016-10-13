# -*- coding: utf-8 -*-

import wx
import wx.aui

from outwiker.gui.toolbars.basetoolbar import BaseToolBar


class WebPageToolBar (BaseToolBar):
    def __init__(self, parent, auiManager):
        super(WebPageToolBar, self).__init__(parent, auiManager)

    def _createPane(self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(3)

    @property
    def name(self):
        return u"webPageToolBar"

    @property
    def caption(self):
        return _(u"Web page")

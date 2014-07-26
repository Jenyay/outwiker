# -*- coding: UTF-8 -*-

import wx
import wx.aui

from outwiker.gui.toolbars.basetoolbar import BaseToolBar


class DiagramToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (DiagramToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(300)


    @property
    def name (self):
        return u"plugin_diagrammer_toolbar"


    @property
    def caption (self):
        return _(u"Diagrammer")

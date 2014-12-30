# -*- coding: UTF-8 -*-

import wx
import wx.aui

from outwiker.gui.toolbars.basetoolbar import BaseToolBar


class DataGraphToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (DataGraphToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(300)


    @property
    def name (self):
        return u"plugin_datagraph_toolbar"


    @property
    def caption (self):
        return _(u"DataGraph")

# -*- coding: utf-8 -*-

import wx
import wx.aui

from outwiker.gui.toolbars.basetoolbar import BaseToolBar


class SimpleToolBar (BaseToolBar):
    '''
    Added in outwiker.gui 1.4
    '''
    def __init__(self, parent, auiManager, name, caption):
        self._name = name
        self._caption = caption
        super(SimpleToolBar, self).__init__(parent, auiManager)

    def _createPane(self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(10)

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

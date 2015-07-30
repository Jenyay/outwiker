#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import wx.aui

from outwiker.gui.toolbars.basetoolbar import BaseToolBar


class LJToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (LJToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(0)


    @property
    def name (self):
        return u"plugin_livejournal_toolbar"


    @property
    def caption (self):
        return _(u"LiveJournal")

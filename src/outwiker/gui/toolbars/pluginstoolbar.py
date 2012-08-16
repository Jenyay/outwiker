#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os.path

import wx
import wx.aui

from .basetoolbar import BaseToolBar
from outwiker.core.system import getImagesDir
from outwiker.core.application import Application


class PluginsToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (PluginsToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(5)


    @property
    def name (self):
        return u"pluginsToolBar"


    @property
    def caption (self):
        return _(u"Plugins")

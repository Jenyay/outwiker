#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os.path

import wx
import wx.aui

from .basetoolbar import BaseToolBar
from outwiker.core.system import getImagesDir


class PluginsToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (PluginsToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name("pluginsToolBar").Caption(_(u"Plugins")).ToolbarPane().Top().Position(5)

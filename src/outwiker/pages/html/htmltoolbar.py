#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os.path

import wx
import wx.aui

from outwiker.gui.basetoolbar import BaseToolBar
from outwiker.core.system import getImagesDir


class HtmlToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (HtmlToolBar, self).__init__(parent, auiManager)


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name("htmlToolBar").Caption(_(u"HTML")).ToolbarPane().Top().Position(1)

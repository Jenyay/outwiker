#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.aui

from outwiker.gui.mainid import MainId
from outwiker.core.system import getImagesDir
from .basetoolbar import BaseToolBar


class GeneralToolBar (BaseToolBar):
    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(0)


    @property
    def name (self):
        return u"generalToolBar"


    @property
    def caption (self):
        return _(u"General")

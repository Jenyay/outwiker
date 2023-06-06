# -*- coding=utf-8 -*-

import wx

from outwiker.core.config import Config
from outwiker.gui.guiconfig import GuiConfig


class WindowSizeSaver:
    def __init__(self, prefix: str, config: Config):
        self._prefix = prefix
        self._config = GuiConfig(config)

    def restoreSize(self, wnd: wx.Window):
        width, height = self._config.loadWindowSize(self._prefix,
                                                    wx.DefaultCoord,
                                                    wx.DefaultCoord)
        wnd.SetSize(width, height)

    def saveSize(self, wnd: wx.Window):
        width, height = wnd.GetSize().Get()
        if width <= 0:
            width = wx.DefaultCoord

        if height <= 0:
            height = wx.DefaultCoord
        self._config.saveWindowSize(self._prefix, width, height)

# -*- coding: utf-8 -*-

import wx


class StaticLineThemed(wx.StaticLine):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LI_HORIZONTAL, theme=None):
        super(StaticLineThemed, self).__init__(parent, id=id, pos=pos,
                                               size=size, style=style)
        self.SetTheme(theme)
        self.SetMinSize((-1, 1))

    def SetTheme(self, theme):
        self._theme = theme
        self.SetBackgroundColour(self._theme.colorStaticLine)

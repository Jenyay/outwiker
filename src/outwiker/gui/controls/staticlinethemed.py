# -*- coding: utf-8 -*-

import wx


class StaticLineThemed(wx.StaticLine):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LI_HORIZONTAL, theme=None):
        super(StaticLineThemed, self).__init__(parent, id=id, pos=pos,
                                               size=size, style=style)
        self._color = wx.Colour(0, 0, 0)
        self.SetTheme(theme)

    def GetDefaultSize(self):
        return self._width

    def SetTheme(self, theme):
        self._theme = theme
        if self._theme is not None:
            self._color = self._theme.colorStaticLine

        self.SetBackgroundColour(self._color)
        if self.IsVertical():
            self.SetMinSize((3, -1))
        else:
            self.SetMinSize((-1, 3))

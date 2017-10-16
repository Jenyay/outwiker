# -*- coding=utf-8 -*-

import wx


class Theme(object):
    def __init__(self):
        self.colorBorder = wx.Colour(0, 0, 0)
        self.colorBorderSelected = wx.Colour(0, 0, 255)
        self.colorBackground = wx.Colour(255, 255, 255)
        self.colorBackgroundSelected = wx.Colour(81, 139, 219)
        self.colorShadow = wx.Colour(200, 200, 200)
        self.colorTextNormal = wx.Colour(0, 0, 0)
        self.colorTextSelected = wx.Colour(0, 0, 0)
        self.roundRadius = 0

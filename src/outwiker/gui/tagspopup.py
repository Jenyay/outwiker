#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .tagscloud import TagsCloud


class TagsPopup (wx.PopupTransientWindow):
    def __init__ (self, parent):
        wx.PopupTransientWindow.__init__ (self, parent)
        self.__tagsCloud = TagsCloud (self)

        sizer = wx.FlexGridSizer (1, 1)
        sizer.Add (self.__tagsCloud, 1, wx.EXPAND)
        sizer.AddGrowableRow (0)
        sizer.AddGrowableCol (0)

        self.SetSizer (sizer)
        self.Layout()


    def setTags (self, taglist):
        self.__tagsCloud.setTags (taglist)


    def Popup (self):
        self.Layout()
        wx.PopupTransientWindow.Popup (self, self.__tagsCloud)

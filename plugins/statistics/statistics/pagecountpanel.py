#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class PageCountPanel (wx.Panel):
    """
    Панель с информацией о количестве страниц
    """
    def __init__ (self, parent):
        super (PageCountPanel, self).__init__ (parent)

        global _
        _ = get_()

        self._createGUI ()


    def _createGUI (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        self.label = wx.StaticText (self, -1, _(u"Page count"))
        self.pageCount = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.pageCount.SetMinSize ((100, -1))

        mainSizer.Add (self.label, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add (self.pageCount, flag=wx.ALIGN_RIGHT | wx.ALL, border=4)

        self.SetSizer (mainSizer)
        self.Layout()

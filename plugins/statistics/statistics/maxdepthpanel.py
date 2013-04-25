#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class MaxDepthPanel (wx.Panel):
    def __init__ (self, parent):
        """
        Панель с информацией о страницах с максимальным уровнем вложенности
        """
        super (MaxDepthPanel, self).__init__ (parent)

        global _
        _ = get_()

        self._createGUI ()


    def _createGUI (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)

        # Вывод наибольшей глубины вложенности
        maxDepthSizer = wx.FlexGridSizer (cols=2)
        maxDepthSizer.AddGrowableCol (0)
        maxDepthSizer.AddGrowableCol (1)

        self.label = wx.StaticText (self, -1, _(u"Max depth of pages"))
        self.maxDepth = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.maxDepth.SetMinSize ((100, -1))

        maxDepthSizer.Add (self.label, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        maxDepthSizer.Add (self.maxDepth, flag=wx.ALIGN_RIGHT | wx.ALL, border=4)

        mainSizer.Add (maxDepthSizer, flag=wx.EXPAND)
        self.SetSizer (mainSizer)
        self.Layout()

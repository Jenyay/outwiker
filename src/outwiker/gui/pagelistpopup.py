# -*- coding: utf-8 -*-

import wx

from .controls.pagelist import PageList
from .controls.popupwindow import PopupWindow


class PageListPopup(PopupWindow):
    def createGUI(self):
        self._pagelist = PageList(self)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self._pagelist.setPageList(pagelist)

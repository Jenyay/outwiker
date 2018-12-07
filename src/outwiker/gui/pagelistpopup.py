# -*- coding: utf-8 -*-

from typing import List

import wx

from .controls.pagelist import PageList, BaseColumn
from .controls.popupwindow import ResizablePopupWindow


class PageListPopup(ResizablePopupWindow):
    def __init__(self, parent, mainWindow, columns: List[BaseColumn]):
        self._columns = columns
        super().__init__(parent, mainWindow)

    def createGUI(self):
        self._pagelist = PageList(self, self._columns)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self._pagelist.setPageList(pagelist)

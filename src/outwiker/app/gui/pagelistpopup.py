# -*- coding: utf-8 -*-

import wx

from outwiker.gui.controls.pagelist import (
    PageList,
    BaseColumn,
    PageListChangeHeadersMixin,
)
from outwiker.gui.controls.popupwindow import ResizablePopupWindow


class PageListPopup(ResizablePopupWindow):
    def createGUI(self):
        self._pagelist = PageList(self)
        self._pagelistMixin = PageListChangeHeadersMixin(self._pagelist)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self._pagelist.setPageList(pagelist)

    def setColumns(self, columns: list[BaseColumn]):
        self._pagelist.setColumns(columns)

    def sortByColumn(self, col_index: int):
        self._pagelist.sortByColumn(col_index)

    def getColumns(self) -> list[BaseColumn]:
        return self._pagelist.getColumns()

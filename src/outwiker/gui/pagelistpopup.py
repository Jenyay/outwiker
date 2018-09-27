# -*- coding: utf-8 -*-

import wx

from .controls.pagelist import (PageList,
                                PageTitleColumn,
                                ParentPageColumn,
                                TagsColumn,
                                ModifyDateColumn)
from .controls.popupwindow import PopupWindow


class PageListPopup(PopupWindow):
    def createGUI(self):
        columns = []
        columns.append(PageTitleColumn(_('Title'), 200, True))
        columns.append(ParentPageColumn(_('Parent'), 200, True))
        columns.append(TagsColumn(_('Tags'), 200, True))
        columns.append(ModifyDateColumn(_('Modify date'), 200, True))

        self._pagelist = PageList(self, columns)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self._pagelist.setPageList(pagelist)

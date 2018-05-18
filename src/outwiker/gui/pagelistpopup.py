# -*- coding: utf-8 -*-

import wx

from .pagelist import PageList


class PageListPopup(wx.PopupTransientWindow):
    def __init__(self, parent):
        super(PageListPopup, self).__init__(parent)

        self.SetWindowStyle(wx.BORDER_SUNKEN)
        self.__pagelist = PageList(self)
        self.__layout()

    def __layout(self):
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self.__pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self.__pagelist.setPageList(pagelist)

    def Popup(self):
        self.Dismiss()
        self.Layout()
        self.SetPosition(self.__getBestPosition())
        super(PageListPopup, self).Popup()

    def __getBestPosition(self):
        """
        Рассчитывает координаты окна таким образом, чтобы оно было около
        курсора, но не вылезало за пределы окна
        """
        mousePosition = wx.GetMousePosition()

        width, height = self.GetSize()
        parent_window_rect = self.GetParent().GetScreenRect()

        if mousePosition.x < parent_window_rect.x + parent_window_rect.width / 2:
            popup_x = mousePosition.x
        else:
            popup_x = mousePosition.x - width

        if mousePosition.y < parent_window_rect.y + parent_window_rect.height / 2:
            popup_y = mousePosition.y
        else:
            popup_y = mousePosition.y - height

        return (popup_x, popup_y)

# -*- coding: UTF-8 -*-

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
        displaySize = wx.GetDisplaySize()

        width, height = self.GetSize()

        # Проверяем разные четверти
        # Слева вверху
        if ((mousePosition.x - width) >= 0 and
                (mousePosition.y - height) >= 0):
            return (mousePosition.x - width, mousePosition.y - height)

        # Справа вверху
        if ((mousePosition.x + width) < displaySize.x and
                (mousePosition.y - height) >= 0):
            return (mousePosition.x, mousePosition.y - height)

        # Слева снизу
        if ((mousePosition.x - width) >= 0 and
                (mousePosition.y + height) < displaySize.y):
            return (mousePosition.x - width, mousePosition.y)

        # Осталось только справа внизу
        return (mousePosition.x, mousePosition.y)

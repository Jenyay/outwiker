# -*- coding: utf-8 -*-

import wx
import wx.adv
import wx.lib.newevent

from outwiker.gui.controls.hyperlink import (HyperLinkCtrl,
                                             EVT_HYPERLINK_LEFT)

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageList(wx.ScrolledWindow):
    def __init__(self, parent):
        super(PageList, self).__init__(
            parent,
            style=wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL
        )

        self.__space = 4

        # Size of the control before layout
        self._oldSize = (-1, -1)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # Список отображаемых элементов
        self.__titleItems = []
        self.__sizer = wx.FlexGridSizer(cols=1)
        self.__sizer.AddGrowableCol(0)

        self.SetSizer(self.__sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_SIZE, self.__onSize)

    def __onSize(self, event):
        newSize = self.GetSize()
        if self._oldSize != newSize:
            self.__updateScroll()
            self._oldSize = newSize

    def __updateScroll(self):
        self.SetScrollbars(0, 0, 0, 0)

        count = len(self.__titleItems)
        if count > 1:
            lastItemY = self.__titleItems[-1].GetPosition()[1]
            lastItemH = (self.__titleItems[-1].GetPosition()[1] -
                         self.__titleItems[-2].GetPosition()[1])

            pixelPerUnitX = 5
            unitX = ((self.__getItemMaxWidth() + 2 * self.__space) /
                     pixelPerUnitX + 1)

            pixelPerUnitY = (lastItemY + lastItemH) / len(self.__titleItems)
            unitY = len(self.__titleItems) + 1

            self.SetScrollbars(pixelPerUnitX,
                               pixelPerUnitY,
                               unitX,
                               unitY,
                               0,
                               0)

    def __getItemMaxWidth(self):
        maxwidth = 0
        for item in self.__titleItems:
            width = item.GetBestSize()[0]
            if width > maxwidth:
                maxwidth = width

        return maxwidth

    def clear(self):
        """
        Удалить все элементы из списка
        """
        for item in self.__titleItems:
            self.__sizer.Detach(item)
            item.Destroy()

        self.__titleItems = []
        self.Layout()
        self.__updateScroll()

    def setPageList(self, pages):
        """
        pages - список страниц, отображаемый в списке
        """
        self.clear()

        for page in pages:
            item = PageTitleItem(self, page)

            self.__titleItems.append(item)
            self.__sizer.Add(
                item,
                0,
                flag=wx.EXPAND | wx.ALL, border=self.__space)

        self.Layout()
        self.__updateScroll()


class PageTitleItem(wx.Panel):
    def __init__(self, parent, page):
        super(PageTitleItem, self).__init__(parent)
        self.__page = page

        self.__color = wx.Colour(0, 0, 255)
        self.__fontSize = 10
        self.__propagationLevel = 15
        self.__backColor = wx.Colour(255, 255, 255)

        self.SetBackgroundColour(self.__backColor)

        url = "/" + page.subpath
        self.__label = HyperLinkCtrl(
            self,
            label=page.title,
            URL=url,
            style=wx.adv.HL_ALIGN_CENTRE | wx.NO_BORDER)

        self.__formatLabel(self.__label)
        self.__label.Bind(EVT_HYPERLINK_LEFT, self.__pageClicked)
        self.Fit()

    def __pageClicked(self, event):
        event = PageClickEvent(page=self.__page)
        event.ResumePropagation(self.__propagationLevel)
        wx.PostEvent(self.GetParent(), event)

    @property
    def page(self):
        return self.__page

    def __formatLabel(self, label):
        font = wx.Font(self.__fontSize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       underline=False)

        label.SetFont(font)
        label.SetToolTip(self.__page.subpath.replace("/", " / "))
        label.SetBackgroundColour(self.__backColor)
        label.SetColours(self.__color, self.__color, self.__color)
        label.AutoBrowse(False)
        label.DoPopup(False)
        label.ReportErrors(False)
        label.EnableRollover(True)
        label.SetUnderlines(False, False, False)
        label.SetSize(label.GetBestSize())

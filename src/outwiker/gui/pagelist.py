#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageList (wx.ScrolledWindow):
    def __init__ (self, parent):
        super (PageList, self).__init__ (parent, style=wx.ALWAYS_SHOW_SB | wx.BORDER_SIMPLE)

        self.__space = 4

        self.SetBackgroundColour (wx.Colour (255, 255, 255))
        # self.SetScrollRate (0, 0)

        # Список отображаемых элементов
        self.__titleItems = []
        self.__sizer = wx.FlexGridSizer (rows = 0, cols=1)
        self.__sizer.AddGrowableCol (0)

        self.SetSizer (self.__sizer)
        self.SetAutoLayout (True)


    def updateScroll (self):
        self.Scroll (0, 0)
        self.SetScrollbars (0, 0, 0, 0)

        count = len (self.__titleItems)
        if count > 1:
            lastItemY = self.__titleItems[-1].GetPositionTuple()[1]
            lastItemH = self.__titleItems[-1].GetPositionTuple()[1] - self.__titleItems[-2].GetPositionTuple()[1]

            pixelPerUnitX = 5
            unitX = (self.__getItemMaxWidth() + 2 * self.__space) / pixelPerUnitX + 1

            pixelPerUnitY = (lastItemY + lastItemH) / len (self.__titleItems)
            unitY = len (self.__titleItems) + 1

            self.SetScrollbars (pixelPerUnitX,
                    pixelPerUnitY,
                    unitX,
                    unitY,
                    0,
                    0)

            
    def __getItemMaxWidth (self):
        maxwidth = 0
        for item in self.__titleItems:
            width = item.GetBestSizeTuple()[0]
            if width > maxwidth:
                maxwidth = width

        return maxwidth



    def clear (self):
        """
        Удалить все элементы из списка
        """
        for item in self.__titleItems:
            self.__sizer.Detach (item)
            item.Destroy()

        self.__titleItems = []
        self.Layout()
        self.updateScroll()


    def setPageList (self, pages):
        """
        pages - список страниц, отображаемый в списке
        """
        self.clear()

        for page in pages:
            item = PageTitleItem (self, page)

            self.__titleItems.append (item)
            self.__sizer.Add (item, 0, flag=wx.EXPAND | wx.ALL, border=self.__space)

        # print "-----"
        # print self.__getItemMaxWidth()
        self.Layout()
        # print self.__getItemMaxWidth()
        # print "-----"
        self.updateScroll()



class PageTitleItem (wx.Panel):
    def __init__ (self, parent, page):
        super (PageTitleItem, self).__init__ (parent)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        self.__color = wx.Colour (0, 0, 0)
        self.__fontSize = 10
        self.__propagationLevel = 15

        self.__label = wx.StaticText (self, -1, page.title)
        self.__colorize (self.__label)

        self.__page = page

        self.__label.Bind (wx.EVT_LEFT_DOWN, self.__pageClicked)
        self.Fit()


    def __pageClicked (self, event):
        event = PageClickEvent (page=self.__page)
        event.ResumePropagation (self.__propagationLevel)
        wx.PostEvent(self.GetParent(), event)


    @property
    def page (self):
        return self.__page


    def __colorize (self, label):
        label.SetForegroundColour (self.__color)

        font = wx.Font (self.__fontSize, 
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                underline=False)

        label.SetFont (font)


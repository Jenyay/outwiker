#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent

TagClickEvent, EVT_TAG_CLICK = wx.lib.newevent.NewEvent()


class TagLabel (wx.HyperlinkCtrl):
    """
    Класс для представления одной метки
    """
    def __init__ (self, parent, title):
        super (TagLabel, self).__init__ (parent, 
                -1, 
                title, 
                title, 
                style=wx.HL_ALIGN_CENTRE | wx.NO_BORDER)

        self.__propagationLevel = 10

        self.__minFontSize = 8
        self.__maxFontSize = 15
        self.__normalBackgroundColor = wx.Colour (255, 255, 255)

        self.__format()


        self.Bind (wx.EVT_HYPERLINK, self.__onMouseLeftDown)

    def __format (self):
        self.SetBackgroundColour(self.__normalBackgroundColor)
        self.SetVisitedColour (self.GetNormalColour())


    def __onMouseLeftDown (self, event):
        newevent = TagClickEvent (text=self.GetLabel())
        newevent.ResumePropagation (self.__propagationLevel)

        wx.PostEvent(self, newevent)


    def setRatio (self, ratio):
        """
        Установить коэффициент, показывающий относительный размер метки.
        Коэффициент должен быть в интервале [0; 1]
        """
        fontsize = int (self.__minFontSize + ratio * (self.__maxFontSize - self.__minFontSize))

        font = wx.Font (fontsize, 
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                underline=False)

        self.SetFont (font)
        self.InvalidateBestSize()
        self.SetSize (self.GetBestSize())


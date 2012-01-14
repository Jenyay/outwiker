#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

class TagLabel (wx.StaticText):
    """
    Класс для представления одной метки
    """
    def __init__ (self, parent, title):
        wx.StaticText.__init__ (self, parent, -1, title)

        self.__minFontSize = 8
        self.__maxFontSize = 15
        self.__color = wx.Colour (0, 0, 255)

        self.SetForegroundColour (self.__color)


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


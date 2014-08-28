# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent

TagLeftClickEvent, EVT_TAG_LEFT_CLICK = wx.lib.newevent.NewEvent()
TagMiddleClickEvent, EVT_TAG_MIDDLE_CLICK = wx.lib.newevent.NewEvent()


class TagLabel (wx.HyperlinkCtrl):
    """
    Класс для представления одной метки
    """
    def __init__ (self, parent, title):
        super (TagLabel, self).__init__ (parent,
                                         wx.ID_ANY,
                                         title,
                                         title,
                                         style=wx.HL_ALIGN_CENTRE | wx.NO_BORDER)

        self.__propagationLevel = 10

        self.__minFontSize = 8
        self.__maxFontSize = 15
        self.__normalBackgroundColor = wx.Colour (255, 255, 255)
        self.__markedBackgroundColor = wx.Colour (250, 255, 36)

        self.__isMarked = False
        self.__format()
        self.Bind (wx.EVT_HYPERLINK, self.__onMouseLeftDown)
        self.Bind (wx.EVT_MIDDLE_DOWN, self.__onMouseMiddleDown)


    def __format (self):
        if self.__isMarked:
            self.SetBackgroundColour(self.__markedBackgroundColor)
        else:
            self.SetBackgroundColour(self.__normalBackgroundColor)

        self.SetVisitedColour (self.GetNormalColour())
        self.Refresh()


    def __onMouseMiddleDown (self, event):
        self.__sendTagEvent (TagMiddleClickEvent)


    def __onMouseLeftDown (self, event):
        self.__sendTagEvent (TagLeftClickEvent)


    def __sendTagEvent (self, eventType):
        newevent = eventType (text=self.GetLabel())
        newevent.ResumePropagation (self.__propagationLevel)
        wx.PostEvent(self.GetParent(), newevent)


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


    def mark (self, marked=True):
        self.__isMarked = marked
        self.__format()


    @property
    def isMarked (self):
        return self.__isMarked

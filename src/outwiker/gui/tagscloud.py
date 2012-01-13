#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent

from outwiker.core.tagslist import TagsList

TagClickEvent, EVT_TAG_CLICK = wx.lib.newevent.NewEvent()


class TagsCloud (wx.ScrolledWindow):
    def __init__ (self, parent):
        wx.ScrolledWindow.__init__ (self, parent, style=wx.BORDER_THEME)

        self.SetScrollRate (0, 0)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        # Отступ от края окна
        self.__margin = 4

        # Отступ между тегами
        self.__space = 10

        self.__minFontSize = 8
        self.__maxFontSize = 15
        self.__normalFont = 10

        # Список классов Tag
        self.__tags = TagsList()

        # Ключ - имя метки, значение - контрол, отображающий эту метку
        self.__labels = {}


    def addTag (self, tag, count):
        """
        Добавить тег в облако
        tag - название тега
        count - количество записей с данным тегов (используется при расчете размера надписи)
        """
        # TODO: Проверить тег на уникальность

        self.__tags.addTag (tag, count)

        newlabel = wx.StaticText (self, -1, tag)
        newlabel.Bind (wx.EVT_LEFT_DOWN, self.__tagClicked)
        self.__labels[tag] = newlabel

        self.layoutTags()


    def __tagClicked (self, event):
        event = TagClickEvent (text=event.GetEventObject().GetLabel())
        wx.PostEvent(self, event)


    def __valignLineLabels (self, labels):
        """
        Выровнять по вертикали метки в одной строке
        """
        maxheight, maxindex = self.__getMaxHeight (labels)
        if maxindex == -1:
            return

        centerY = labels[maxindex].GetPositionTuple()[1] + maxheight / 2

        for label in labels:
            currx, curry = label.GetPositionTuple()
            height = label.GetSizeTuple()[1]
            label.SetPosition ((currx, centerY - height / 2))


    def __getMaxHeight (self, labels):
        maxheight = 0
        maxindex = -1

        if len (labels) == 0:
            return (maxheight, maxindex)

        for label, index in zip (labels, range (len (labels))):
            height = label.GetSizeTuple()[1]
            if height > maxheight:
                maxheight = height
                maxindex = index

        return (maxheight, maxindex)


    def __calcSizeRatio (self, count):
        maxcount = self.__tags.getMaxCount()
        ratio = 1

        if maxcount != 0:
            ratio = count / maxcount

        return ratio


    def __setSizeLabels (self):
        for tagname, count in self.__tags:
            label = self.__labels[tagname]
            ratio = self.__calcSizeRatio (count)
            self.__formatLabel (label, ratio)


    def __formatLabel (self, label, ratio):
        fontsize = int (self.__minFontSize + ratio * (self.__maxFontSize - self.__minFontSize))

        font = wx.Font (fontsize, 
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                underline=False)

        label.SetFont (font)
        label.SetForegroundColour (wx.Colour (0, 0, 255))


    def layoutTags (self):
        """
        Расположение тегов в окне
        """
        self.Scroll (0, 0)
        self.SetScrollbars (0, 0, 0, 0)

        self.__setSizeLabels()

        # Дважды перемещаем метки, чтобы учесть, что может появиться полоса прокрутки
        self.__moveLabels()
        self.__moveLabels()


    def __moveLabels (self):
        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self.__margin
        currenty = self.__margin

        linesCount = 1

        maxwidth = self.GetClientSizeTuple()[0] - self.__margin

        for tagname, count in self.__tags:
            label = self.__labels[tagname]
            newRightBorder = currentx + label.GetSizeTuple()[0]

            if newRightBorder > maxwidth and len (currentLine) != 0:
                self.__valignLineLabels (currentLine)

                currentx = self.__margin
                currenty += self.__getMaxHeight (currentLine)[0] + self.__space

                currentLine = []
                linesCount += 1

            label.SetPosition ((currentx, currenty))
            currentLine.append (label)
            currentx += label.GetSizeTuple()[0] + self.__space

        if len (self.__tags) != 0:
            commonheight = currenty + self.__space
            lineheight = commonheight / linesCount

            self.SetScrollbars (0, 
                    lineheight,
                    0,
                    linesCount)

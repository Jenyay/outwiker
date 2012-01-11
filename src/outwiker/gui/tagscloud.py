#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import  wx.lib.newevent

TagClickEvent, EVT_TAG_CLICK = wx.lib.newevent.NewEvent()


class TagsCloud (wx.ScrolledWindow):
    def __init__ (self, parent):
        wx.ScrolledWindow.__init__ (self, parent, style=wx.BORDER_SIMPLE)

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
        self.__tags = []


    def addTag (self, tag, count):
        """
        Добавить тег в облако
        tag - название тега
        count - количество записей с данным тегов (используется при расчете размера надписи)
        """
        newlabel = wx.StaticText (self, -1, tag)
        newlabel.Bind (wx.EVT_LEFT_DOWN, self.__tagClicked)

        newTag = Tag (tag, count, newlabel)

        self.__tags.append (newTag)
        self.__tags.sort (self.__compareTags)

        self.__formatLabel (newTag)
        self.layoutTags()


    def __tagClicked (self, event):
        event = TagClickEvent (text=event.GetEventObject().GetLabel())
        wx.PostEvent(self, event)


    def __calcFontSize (self, tag):
        maxcount = self.__getMaxCount()
        mincount = 1

        if maxcount != 0:
            size = int (self.__minFontSize + 
                tag.count * (self.__maxFontSize - self.__minFontSize) / maxcount)
        else:
            size = self.__normalFont

        return size


    def __getMaxCount (self):
        count = 0
        for tag in self.__tags:
            if tag.count > count:
                count = tag.count

        return count


    def __formatLabel (self, tag):
        fontsize = self.__calcFontSize (tag)

        font = wx.Font (fontsize, 
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                underline=False)

        tag.label.SetFont (font)
        tag.label.SetForegroundColour (wx.Colour (0, 0, 255))


    def __valignLineLabels (self, tags):
        """
        Выровнять по вертикали метки в одной строке
        """
        maxheight, maxindex = self.__getMaxHeight (tags)
        if maxindex == -1:
            return

        centerY = tags[maxindex].label.GetPositionTuple()[1] + maxheight / 2

        for tag in tags:
            currx, curry = tag.label.GetPositionTuple()
            height = tag.label.GetSizeTuple()[1]
            tag.label.SetPosition ((currx, centerY - height / 2))


    def __getMaxHeight (self, tags):
        maxheight = 0
        maxindex = -1

        if len (tags) == 0:
            return (maxheight, maxindex)

        for tag, index in zip (tags, range (len (tags))):
            height = tag.label.GetSizeTuple()[1]
            if height > maxheight:
                maxheight = height
                maxindex = index

        return (maxheight, maxindex)


    def layoutTags (self):
        """
        Расположение тегов в окне
        """
        self.Scroll (0, 0)
        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self.__margin
        currenty = self.__margin

        linesCount = 0

        maxwidth = self.GetClientSizeTuple()[0] - self.__margin

        for tag in self.__tags:
            newRightBorder = currentx + tag.label.GetSizeTuple()[0]

            if newRightBorder > maxwidth and len (currentLine) != 0:
                self.__valignLineLabels (currentLine)

                currentx = self.__margin
                currenty += self.__getMaxHeight (currentLine)[0] + self.__space

                currentLine = []
                linesCount += 1

            tag.label.SetPosition ((currentx, currenty))
            currentLine.append (tag)
            currentx += tag.label.GetSizeTuple()[0] + self.__space

        if len (self.__tags) != 0:
            self.SetScrollbars (0, 
                    self.__tags[0].label.GetSizeTuple()[1] + self.__space,
                    0,
                    linesCount + 1)


    def __compareTags (self, tag1, tag2):
        """
        Функция для сравнения экземпляров класса Tag
        """
        name1 = tag1.name.lower()
        name2 = tag2.name.lower()

        if name1 < name2:
            return -1

        if name1 > name2:
            return 1

        return 0




class Tag (object):
    def __init__ (self, name, count, label):
        """
        name - название метки
        count - количество записей с такой меткой
        label - контрол, отображающий данную метку
        """
        self.__name = name
        self.__count = count
        self.__label = label


    @property
    def name (self):
        return self.__name

    
    @property
    def count (self):
        return self.__count


    @property
    def label (self):
        return self.__label

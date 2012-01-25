#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .taglabel import TagLabel


class TagsCloud (wx.ScrolledWindow):
    def __init__ (self, parent):
        super (TagsCloud, self).__init__ (parent, style=wx.BORDER_THEME)

        self.SetScrollRate (0, 0)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        # Отступ от края окна
        self.__margin = 4

        # Отступ между тегами
        self.__space = 10

        self.__tags = None

        # Ключ - имя метки, значение - контрол, отображающий эту метку
        self.__labels = {}

        self.Bind (wx.EVT_SIZE, self.__onSize)


    def __onSize (self, event):
        self.__layoutTags()


    def setTags (self, taglist):
        """
        Добавить тег в облако
        """
        oldy = self.GetScrollPos (wx.VERTICAL)
        self.clear()

        self.__tags = taglist

        for tag in taglist:
            newlabel = TagLabel(self, tag)
            self.__labels[tag] = newlabel

        self.__layoutTags()
        self.Scroll (-1, oldy)


    def mark (self, tag, marked=True):
        """
        Выделить метку
        """
        assert tag.lower().strip() in self.__labels.keys()
        self.__labels[tag.lower().strip()].mark(marked)


    def clearMarks (self):
        """
        Убрать все выделения с меток
        """
        map (lambda label: label.mark(False), self.__labels.values())


    def clear(self):
        map (lambda label: label.Destroy(), self.__labels.values())

        self.__labels = {}
        self.__tags = None


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


    def __getMaxCount (self):
        count = 0
        for tag in self.__tags:
            if len(self.__tags[tag]) > count:
                count = len(self.__tags[tag])

        return count


    def __calcSizeRatio (self, count):
        assert self.__tags != None

        maxcount = self.__getMaxCount()
        ratio = 1

        if maxcount != 0:
            ratio = float(count) / maxcount

        return ratio


    def __setSizeLabels (self):
        for tagname in self.__tags:
            count = len (self.__tags[tagname])
            ratio = self.__calcSizeRatio (count)

            label = self.__labels[tagname]
            label.setRatio (ratio)


    def __layoutTags (self):
        """
        Расположение тегов в окне
        """
        self.SetScrollbars (0, 0, 0, 0)

        if self.__tags == None:
            return

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

        for tagname in self.__tags:
            count = len (self.__tags[tagname])
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
            commonheight = currenty + self.__getMaxHeight (currentLine)[0] + self.__space
            lineheight = commonheight / linesCount

            self.SetScrollbars (0, 
                    lineheight,
                    0,
                    linesCount + 1)


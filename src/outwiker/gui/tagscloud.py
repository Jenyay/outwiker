#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

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

        # Список классов Tag
        self.__tags = []


    def addTag (self, tag, count):
        """
        Добавить тег в облако
        tag - название тега
        count - количество записей с данным тегов (используется при расчете размера надписи)
        """
        newlabel = wx.StaticText (self, -1, tag)
        self.__formatLabel (newlabel)

        self.__tags.append (Tag (tag, count, newlabel) )
        self.__tags.sort (self.__compareTags)
        self.layoutTags()


    def __formatLabel (self, label):
        font = wx.Font (10, 
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                underline=True)
        label.SetFont (font)
        label.SetForegroundColour (wx.Colour (0, 0, 255))


    def layoutTags (self):
        """
        Расположение тегов в окне
        """
        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self.__margin
        currenty = self.__margin

        linesCount = 0

        maxwidth = self.GetClientSizeTuple()[0] - self.__margin

        for tag in self.__tags:
            newRightBorder = currentx + tag.label.GetSizeTuple()[0]

            if newRightBorder > maxwidth and len (currentLine) != 0:
                # TODO: Выровнять текущую строку

                currentx = self.__margin

                # TODO:  Сдвиг по высоте рассчитывать с учетом 
                # максимального размера метки по вертикали на линии

                currenty += currentLine[0].label.GetSizeTuple()[1] + self.__space

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

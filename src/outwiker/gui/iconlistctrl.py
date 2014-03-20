#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.grid

import outwiker.core.system


class IconButton (wx.PyControl):
    """
    Кнопка с одной иконкой
    """
    def __init__ (self, parent, fname, width, height):
        wx.PyControl.__init__ (self, parent, id=wx.NewId(), style=wx.BORDER_NONE)
        self.fname = fname
        self.image = wx.Bitmap (fname)

        # Выбрана ли данная иконка?
        self.__selected = False

        # Оформление
        self.normalBackground = wx.Colour (255, 255, 255)
        self.selectedBackground = wx.Colour (200, 200, 200)

        self.SetToolTipString (self.__getToolTipText (fname))

        self.SetSize ((width, height))
        self.Bind (wx.EVT_PAINT, self.__onPaint)


    def __getToolTipText (self, fname):
        """
        Возвращет текст всплывающей подсказки для кнопки по имени файла
        """
        text = os.path.basename (fname)

        # Отбросим расширение файла
        dotPos = text.rfind (".")
        if dotPos != -1:
            text = text[: dotPos]

        return text


    def __onPaint (self, event):
        dc = wx.PaintDC (self)

        dc.SetBrush (wx.Brush (self.selectedBackground if self.selected else self.normalBackground) )
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle (0, 0, self.Size[0], self.Size[1])

        (xsize, ysize) = self.GetSizeTuple()
        posx = (xsize - self.image.GetWidth()) / 2
        posy = (ysize - self.image.GetHeight()) / 2

        dc.DrawBitmap(self.image, posx, posy, True)


    @property
    def selected (self):
        return self.__selected


    @selected.setter
    def selected (self, value):
        if value != self.__selected:
            self.__selected = value
            self.Refresh()


class IconListCtrl (wx.ScrolledWindow):
    """
    Список иконок
    """
    def __init__ (self, parent):
        wx.ScrolledWindow.__init__ (self, parent, style = wx.BORDER_THEME)

        self.cellWidth = 32
        self.cellHeight = 32
        self.margin = 1

        self.SetScrollRate (0, 0)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        # Список картинок, которые хранятся в окне
        self.buttons = []

        self.imagesDir = outwiker.core.system.getImagesDir()
        self.iconspath = os.path.join (self.imagesDir, "iconset")
        self.defaultIcon = os.path.join (self.imagesDir, "page.png")

        # Иконка по умолчанию
        self.defalultImage = u"_page.png"

        self.__updateList()

        #self.SetFocus()
        self.Bind (wx.EVT_SIZE, self.onSize)

    
    def onSize (self, event):
        self.__layout()


    def __updateList (self):
        for button in self.buttons:
            button.Unbind (wx.EVT_LEFT_DOWN, self.__onButtonClick)
            button.Hide()
            button.Close()

        self.buttons = []

        files = [fname for fname in os.listdir (self.iconspath)]
        files.sort(reverse=True)

        for fname in files:
            fullpath = os.path.join (self.iconspath, fname)
            button = self.__addButton (fullpath)

            if fname == self.defalultImage:
                button.selected = True

        self.__layout()
        self.__selectedButton.SetFocus()


    def __addButton (self, fname):
        """
        Добавить кнопку с картинкой fname (полный путь)
        """
        button = IconButton (self, fname, self.cellWidth, self.cellHeight)
        button.Bind (wx.EVT_LEFT_DOWN, self.__onButtonClick)
        self.buttons.insert (0, button)

        return button

    
    def __onButtonClick (self, event):
        for button in self.buttons:
            if button.GetId() == event.GetId():
                button.selected = True
                button.SetFocus()
            else:
                button.selected = False



    def __layout (self):
        currx = 0
        curry = 0

        rowcount = 1

        windowWidth = self.GetClientSizeTuple()[0]

        for button in self.buttons:
            buttonWidth = button.Size[0]

            if buttonWidth + currx + self.margin >= windowWidth:
                currx = 0
                curry += self.cellHeight + self.margin
                rowcount += 1

            button.SetPosition ((currx, curry))
            currx += buttonWidth + self.margin

        self.SetScrollbars (self.cellWidth, self.cellHeight, 1, rowcount + 1)


    @property
    def icon (self):
        selButton = self.__selectedButton
        if selButton != None:
            return selButton.fname


    def addCurrentIcon (self, fname):
        """
        Добавить иконку и сделать ее выбранной по умолчанию
        """
        assert fname != None
        
        button = self.__addButton (fname)
        self.__layout()
        self.__selectedButton.selected = False
        button.selected = True
        button.SetFocus()


    @property
    def __selectedButton (self):
        for button in self.buttons:
            if button.selected:
                return button

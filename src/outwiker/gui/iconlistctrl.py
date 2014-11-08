# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.grid

from outwiker.core.system import getImagesDir


class IconButton (wx.PyControl):
    """
    Button with single icons
    """
    def __init__ (self, parent, fname, width, height):
        wx.PyControl.__init__ (self, parent, id=wx.NewId(), style=wx.BORDER_NONE)
        self.fname = fname

        # Disable wxPython message about the invalid picture format
        wx.Log_EnableLogging(False)
        self.image = wx.Bitmap (fname)
        wx.Log_EnableLogging(True)

        if not self.image.IsOk():
            print _(u'Invalid icon file: {}').format (fname)
            raise ValueError

        # Выбрана ли данная иконка?
        self.__selected = False

        # Оформление
        self.normalBackground = wx.Colour (255, 255, 255)
        self.selectedBackground = wx.Colour (160, 190, 255)
        self.borderColor = wx.Colour (0, 0, 255)

        self.SetToolTipString (self.__getToolTipText (fname))

        self.SetSize ((width, height))
        self.Bind (wx.EVT_PAINT, self.__onPaint)


    def __getToolTipText (self, fname):
        """
        Return the text of the tooltip with file name
        """
        text = os.path.basename (fname)

        # Отбросим расширение файла
        dotPos = text.rfind (".")
        if dotPos != -1:
            text = text[: dotPos]

        if text == "__icon":
            text = _(u"Curent icon")
        elif text == u"_page":
            text = _(u"Default icon")

        return text


    def __onPaint (self, event):
        assert self.image.IsOk()

        dc = wx.PaintDC (self)

        dc.SetBrush (wx.Brush (self.selectedBackground if self.selected else self.normalBackground))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle (0, 0, self.Size[0], self.Size[1])

        (xsize, ysize) = self.GetSizeTuple()
        posx = (xsize - self.image.GetWidth()) / 2
        posy = (ysize - self.image.GetHeight()) / 2

        dc.DrawBitmap(self.image, posx, posy, True)

        if self.selected:
            dc.SetPen (wx.Pen (self.borderColor))
            dc.SetBrush (wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle (0, 0, self.Size[0], self.Size[1])


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
    Control with icons for pages
    """
    def __init__ (self, parent, multiselect=False):
        wx.ScrolledWindow.__init__ (self, parent, style = wx.BORDER_THEME | wx.SUNKEN_BORDER)

        self.cellWidth = 32
        self.cellHeight = 32
        self.margin = 1
        self.multiselect = multiselect

        # Path to current page icon
        self._currentIcon = None

        self._lastClickedButton = None

        self.SetScrollRate (0, 0)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        # Список картинок, которые хранятся в окне
        self.buttons = []

        self.defaultIcon = os.path.join (getImagesDir(), "page.png")

        self.Bind (wx.EVT_SIZE, self.__onSize)


    def __onSize (self, event):
        self.__layout()


    def clear (self):
        """
        Remove old buttons with icons.
        """
        for button in self.buttons:
            button.Unbind (wx.EVT_LEFT_DOWN, handler=self.__onButtonClick)
            button.Hide()
            button.Destroy()

        self.buttons = []
        self._lastClickedButton = None
        self.Scroll (0, 0)


    def setIconsList (self, icons):
        self.clear()

        for fname in reversed (icons):
            self.__addButton (fname)

        self.setCurrentIcon (self._currentIcon)
        if len (self.buttons) != 0:
            self.__selectSingleButton (self.buttons[0].GetId())

        self.__layout()
        self.Scroll (0, 0)


    def __addButton (self, fname):
        """
        Add the button with icons fname (full path)
        """
        try:
            button = IconButton (self, fname, self.cellWidth, self.cellHeight)
        except ValueError:
            return

        button.Bind (wx.EVT_LEFT_DOWN, self.__onButtonClick)
        self.buttons.insert (0, button)


    def __onButtonClick (self, event):
        ctrl = wx.GetKeyState (wx.WXK_CONTROL)
        shift = wx.GetKeyState (wx.WXK_SHIFT)

        if (not self.multiselect or
                (not ctrl and not shift)):
            self.__selectSingleButton (event.GetId())
        elif ctrl:
            self.__toggleSelectionButton (event.GetId())
        elif shift and self._lastClickedButton is not None:
            self.__selectFromTo (self._lastClickedButton.GetId(), event.GetId())


    def __selectSingleButton (self, buttonid):
        for button in self.buttons:
            if button.GetId() == buttonid:
                button.selected = True
                button.SetFocus()
                self._lastClickedButton = button
            else:
                button.selected = False


    def __toggleSelectionButton (self, buttonid):
        for button in self.buttons:
            if button.GetId() == buttonid:
                button.selected = not button.selected
                button.SetFocus()
                self._lastClickedButton = button
                break


    def __selectFromTo (self, fromId, toId):
        fromIndex = -1
        toIndex = -1

        for index, button in enumerate (self.buttons):
            if fromId == button.GetId():
                fromIndex = index

            if toId == button.GetId():
                toIndex = index

        assert fromIndex != -1
        assert toIndex != -1

        minIndex = min (fromIndex, toIndex)
        maxIndex = max (fromIndex, toIndex)

        for button in self.buttons[minIndex: maxIndex + 1]:
            button.selected = True
            button.SetFocus()
            self._lastClickedButton = button


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


    def getSelection (self):
        """
        Return list of the selected icons
        """
        return [button.fname for button in self.buttons if button.selected]


    def setCurrentIcon (self, fname):
        """
        Add the icon and make it selected default
        """
        self._currentIcon = fname
        if self._currentIcon is None:
            return

        self.__addButton (self._currentIcon)
        self.__layout()
        self.__selectSingleButton (self.buttons[0].GetId())

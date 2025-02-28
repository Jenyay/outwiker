# -*- coding: utf-8 -*-

import logging
import os.path
from typing import Union

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.defines import ICON_DEFAULT
from outwiker.core.system import getBuiltinImagePath
from outwiker.core.iconcontroller import IconController
from outwiker.gui.defines import ICONS_HEIGHT, ICONS_WIDTH
from outwiker.gui.images import readImage
from outwiker.gui.theme import Theme

IconSelectedEvent, EVT_ICON_SELECTED = NewEvent()
IconDoubleClickEvent, EVT_ICON_DOUBLE_CLICK = NewEvent()


class IconButton:
    """
    Button with single icons
    """

    def __init__(self, parent, fname, width, height, theme=None):
        self._parent = parent
        self._fname = fname
        self._width = width
        self._height = height

        self._invalidFileName = getBuiltinImagePath("cross.png")

        self._normalBackground = wx.Colour(255, 255, 255)
        self._selectedBackground = wx.Colour(160, 190, 255)
        self._borderColor = wx.Colour(0, 0, 255)

        if theme is not None:
            self._normalBackground = theme.colorBackground
            self._selectedBackground = theme.colorBackgroundSelected
            self._borderColor = theme.get(Theme.SECTION_GENERAL, Theme.CONTROL_BORDER_SELECTED_COLOR)

        self._x = 0
        self._y = 0
        self._image = None

        # Выбрана ли данная иконка?
        self.__selected = False

    def _createImage(self, fname):
        # Disable wxPython message about the invalid picture format
        wx.Log.EnableLogging(False)
        image = readImage(fname, ICONS_WIDTH, ICONS_HEIGHT)
        wx.Log.EnableLogging(True)

        if not image.IsOk():
            logging.error("Invalid icon file: %s", fname)
            image = readImage(self._invalidFileName, ICONS_WIDTH, ICONS_HEIGHT)

        return image

    def paint(self, dc):
        if self._image is None:
            self._image = self._createImage(self._fname)

        assert self._image.IsOk()

        dc.SetBrush(
            wx.Brush(
                self._selectedBackground if self.selected else self._normalBackground
            )
        )

        dc.SetPen(wx.TRANSPARENT_PEN)

        dc.DrawRectangle(self._x, self._y, self._width, self._height)

        posx = self._x + (self._width - self._image.GetWidth()) // 2
        posy = self._y + (self._height - self._image.GetHeight()) // 2

        dc.DrawBitmap(self._image, posx, posy, True)

        if self.selected:
            dc.SetPen(wx.Pen(self._borderColor))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle(self._x, self._y, self._width, self._height)

        dc.SetBrush(wx.NullBrush)
        dc.SetPen(wx.NullPen)

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        if value != self.__selected:
            self.__selected = value

    def SetPosition(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def getToolTipText(self):
        """
        Return the text of the tooltip with file name
        """
        text_src = os.path.basename(self._fname)

        # Отбросим расширение файла
        dotPos = text_src.rfind(".")
        if dotPos != -1:
            text = text_src[:dotPos]

        if text == "__icon":
            text = _("Custom icon")
        elif text_src == ICON_DEFAULT:
            text = _("Default icon")
        else:
            text = IconController.display_name(self._fname)

        return text

    @property
    def iconFileName(self):
        return self._fname


class IconListCtrl(wx.ScrolledWindow):
    """
    Control with icons for pages
    """

    def __init__(self, parent, multiselect=False, theme=None):
        wx.ScrolledWindow.__init__(self, parent, style=wx.BORDER_THEME)
        self._theme = theme
        self._propagationLevel = 20

        self._backgroundColor = wx.Colour(255, 255, 255)
        if self._theme is not None:
            self._backgroundColor = self._theme.colorBackground

        self._canvas = wx.Panel(self)
        self._canvas.SetSize((0, 0))
        self._canvas.SetBackgroundColour(self._backgroundColor)
        self._canvas.Bind(wx.EVT_PAINT, handler=self.__onPaint)
        self._canvas.Bind(wx.EVT_LEFT_DOWN, handler=self.__onCanvasClick)
        self._canvas.Bind(wx.EVT_LEFT_DCLICK, handler=self.__onCanvasDoubleClick)
        self._canvas.Bind(wx.EVT_MOTION, handler=self.__onMouseMove)

        self.Bind(wx.EVT_SCROLLWIN, handler=self.__onScroll)

        self.cellWidth = 32
        self.cellHeight = 32
        self.margin = 1
        self.multiselect = multiselect

        # Size of the control before icons layout
        self._oldSize = (-1, -1)

        # Path to current page icon
        self._currentIcon = None

        self._lastClickedButton = None

        # self.SetScrollRate(0, 0)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # Список картинок, которые хранятся в окне
        self.buttons = []
        self._iconFileNames = []

        self.defaultIcon = getBuiltinImagePath("page.svg")

        self.Bind(wx.EVT_SIZE, self.__onSize)

    def _findButtonByFileName(self, fname: str) -> Union[IconButton, None]:
        fname = os.path.abspath(fname)
        for button in self.buttons:
            if os.path.abspath(button.iconFileName) == fname:
                return button

        return None

    def __onSize(self, event):
        newSize = self.GetSize()
        if self._oldSize != newSize:
            self.__layout()
            self._oldSize = newSize

    def __onPaint(self, event):
        dc = wx.AutoBufferedPaintDCFactory(self._canvas)

        y0 = self.GetScrollPos(wx.VERTICAL) * (self.cellHeight + self.margin)
        y1 = y0 + self.GetClientSize()[1]

        dc.SetBrush(wx.Brush(self._backgroundColor))
        dc.SetPen(wx.TRANSPARENT_PEN)

        dc.DrawRectangle(0, y0, self._canvas.GetSize()[0], self._canvas.GetSize()[1])

        dc.SetBrush(wx.NullBrush)
        dc.SetPen(wx.NullPen)

        for button in self.buttons:
            if button.y >= y0 and button.y <= y1:
                button.paint(dc)

    def __onMouseMove(self, event):
        button = self._getButtonByCoord(event.GetPosition()[0], event.GetPosition()[1])
        self._canvas.SetToolTip("")

        if button is not None:
            self._canvas.SetToolTip(button.getToolTipText())

    def clear(self):
        """
        Remove old buttons with icons.
        """
        self.buttons = []
        self._iconFileNames = []
        self._lastClickedButton = None
        self.Scroll(0, 0)

    def setIconsList(self, iconFileNames):
        self.clear()
        self._iconFileNames = iconFileNames[:]

        for fname in reversed(self._iconFileNames):
            self.__addButton(fname)

        self.__layout()
        self.Scroll(0, 0)

    def __addButton(self, fname):
        """
        Add the button with icons fname (full path)
        """
        try:
            button = IconButton(
                self._canvas, fname, self.cellWidth, self.cellHeight, self._theme
            )
        except ValueError:
            return

        self.buttons.insert(0, button)
        return button

    def _getButtonByCoord(self, x, y):
        for button in self.buttons:
            if (
                x >= button.x
                and x <= button.x + button.width
                and y >= button.y
                and y <= button.y + button.height
            ):
                return button

    def __onSelectIcon(self, event):
        ctrl = wx.GetKeyState(wx.WXK_CONTROL)
        shift = wx.GetKeyState(wx.WXK_SHIFT)

        button = self._getButtonByCoord(event.GetPosition()[0], event.GetPosition()[1])

        if button is None:
            return

        if not self.multiselect or (not ctrl and not shift):
            self.__selectSingleButton(button)
        elif ctrl:
            self.__toggleSelectionButton(button)
        elif shift and self._lastClickedButton is not None:
            self.__selectFromTo(self._lastClickedButton, button)

        self._refreshCanvas()
        self.SetFocus()

    def __onCanvasClick(self, event):
        self.__onSelectIcon(event)
        self._sendIconSelectedEvent()

    def __onCanvasDoubleClick(self, event):
        self.__onSelectIcon(event)
        self._sendDoubleClickEvent()

    def __onScroll(self, event):
        self._refreshCanvas()
        event.Skip()

    def _refreshCanvas(self):
        self._canvas.Refresh(False)

    def __selectSingleButton(self, selectedButton):
        for button in self.buttons:
            if button is selectedButton:
                button.selected = True
                self._lastClickedButton = button
            else:
                button.selected = False

    def __toggleSelectionButton(self, button):
        button.selected = not button.selected
        self._lastClickedButton = button

    def __selectFromTo(self, fromButton, toButton):
        fromIndex = -1
        toIndex = -1

        for index, button in enumerate(self.buttons):
            if button is fromButton:
                fromIndex = index

            if button is toButton:
                toIndex = index

        assert fromIndex != -1
        assert toIndex != -1

        minIndex = min(fromIndex, toIndex)
        maxIndex = max(fromIndex, toIndex)

        for button in self.buttons[minIndex : maxIndex + 1]:
            button.selected = True
            self._lastClickedButton = button

    def __layout(self):
        self.Unbind(wx.EVT_SCROLLWIN, handler=self.__onScroll)

        currx = 0
        curry = 0
        windowWidth = self.GetClientSize()[0]

        # Row size in cells(columns count)
        colsCount = (windowWidth - self.margin) // (self.cellWidth + self.margin)
        if colsCount <= 0:
            return

        rowsCount = len(self.buttons) // colsCount + 1

        for n, button in enumerate(self.buttons):
            row = n // colsCount
            col = n % colsCount

            currx = self.margin + col * (self.cellWidth + self.margin)
            curry = self.margin + row * (self.cellHeight + self.margin)

            button.x = currx
            button.y = curry

        self.Scroll(0, 0)
        self._canvas.SetSize(windowWidth, rowsCount * (self.cellHeight + self.margin))

        self.SetScrollbars(self.cellWidth, self.cellHeight + self.margin, 1, rowsCount)
        self._refreshCanvas()

        self.Bind(wx.EVT_SCROLLWIN, handler=self.__onScroll)

    def getSelection(self):
        """
        Return list of the selected icons
        """
        return [button.iconFileName for button in self.buttons if button.selected]

    def setCurrentIcon(self, fname):
        """
        Add the icon and make it selected default
        """
        self._currentIcon = fname
        if self._currentIcon is None:
            return

        currentButton = self._findButtonByFileName(fname)
        if currentButton is None:
            self._iconFileNames.insert(0, fname)
            self.__addButton(self._currentIcon)
            self.__layout()
            self.__selectSingleButton(self.buttons[0])
        else:
            self.__selectSingleButton(currentButton)
            dy = self.GetScrollPixelsPerUnit()[1]
            if dy != 0:
                self.Scroll(0, currentButton.y // dy)

        self._sendIconSelectedEvent()

    def _sendIconSelectedEvent(self):
        newevent = IconSelectedEvent(icons=self.getSelection())
        newevent.ResumePropagation(self._propagationLevel)
        wx.PostEvent(self, newevent)

    def _sendDoubleClickEvent(self):
        newevent = IconDoubleClickEvent(icons=self.getSelection())
        newevent.ResumePropagation(self._propagationLevel)
        wx.PostEvent(self, newevent)

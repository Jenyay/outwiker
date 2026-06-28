# -*- coding: utf-8 -*-

import os
import math
from typing import Collection, Dict, List, Optional, Tuple
from collections.abc import Iterable
from datetime import datetime

import wx
import wx.lib.newevent

from outwiker.core.system import getBuiltinImagePath
from outwiker.core.tagslist import TagsList
from outwiker.gui.defines import TAGS_CLOUD_MODE_CONTINUOUS, TAGS_CLOUD_MODE_LIST
from outwiker.gui.images import readImage
from outwiker.gui.theme import Theme

TagLeftDownEvent, EVT_TAG_LEFT_DOWN = wx.lib.newevent.NewEvent()
TagLeftUpEvent, EVT_TAG_LEFT_UP = wx.lib.newevent.NewEvent()

TagRightDownEvent, EVT_TAG_RIGHT_DOWN = wx.lib.newevent.NewEvent()
TagRightUpEvent, EVT_TAG_RIGHT_UP = wx.lib.newevent.NewEvent()

TagMiddleDownEvent, EVT_TAG_MIDDLE_DOWN = wx.lib.newevent.NewEvent()
TagMiddleUpEvent, EVT_TAG_MIDDLE_UP = wx.lib.newevent.NewEvent()

TagAddEvent, EVT_TAG_ADD = wx.lib.newevent.NewEvent()
TagRemoveEvent, EVT_TAG_REMOVE = wx.lib.newevent.NewEvent()


class _LabelGeometry:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.center_y = 0
        self.arc_width = 0
        self.button_border_x = 0
        self.button_center_x = 0
        self.button_center_y = 0
        self.text_left = 0
        self.button_add_left = 0
        self.button_add_right = 0
        self.button_add_top = 0
        self.button_add_bottom = 0
        self.button_remove_left = 0
        self.button_remove_right = 0
        self.button_remove_top = 0
        self.button_remove_bottom = 0
        self.font_size = 0
        self.text_width = 0


class TagLabel2:
    def __init__(
        self,
        parent: wx.Window,
        label: str,
        use_buttons: bool = True,
        min_font_size: int = 8,
        max_font_size: int = 16,
        x: int = 0,
        y: int = 0,
    ):
        self._parent = parent
        self._label = label
        self._use_buttons = use_buttons
        self._is_marked = False
        self._is_hover = False
        self._is_hover_button = False

        self._x = x
        self._y = y
        self._visible = True

        self._propagationLevel = 10
        self._ratio = 1.0

        self._geometry = _LabelGeometry()
        self.setFontSize(min_font_size, max_font_size)

    @property
    def geometry(self) -> _LabelGeometry:
        return self._geometry

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def label(self) -> str:
        return self._label

    @property
    def isUseButtons(self) -> bool:
        return self._use_buttons

    @property
    def isButtonHovered(self) -> bool:
        return self._is_hover_button

    @property
    def isHovered(self) -> bool:
        return self._is_hover

    def setHover(self, value: bool):
        self._is_hover = value

    def isVisible(self) -> bool:
        return self._visible

    def Move(self, x: int, y: int):
        self._x = x
        self._y = y

    def getSize(self) -> Tuple[int, int]:
        return (self.geometry.width, self.geometry.height)

    def getPosition(self) -> Tuple[int, int]:
        return (self._x, self._y)

    def getPositionMax(self) -> Tuple[int, int]:
        return (self._x + self.geometry.width, self._y + self.geometry.height)

    def Show(self, visible=True):
        self._visible = visible

    def getLabel(self) -> str:
        return self._label

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._min_font_size = min(min_font_size, max_font_size)
        self._max_font_size = max(min_font_size, max_font_size)
        self._calc_geometry()

    def _calc_em(self) -> int:
        return self._calc_text_size("Q", self._max_font_size)[1]

    def _calc_text_size(self, text: str, font_size: int) -> Tuple[int, int]:
        with wx.ClientDC(self._parent) as dc:
            font = wx.Font(wx.FontInfo(font_size))
            dc.SetFont(font)
            return dc.GetTextExtent(text)

    def _em2px(self, em: float) -> int:
        return int(em * self._em)

    def _calc_geometry(self):
        self._em = self._calc_em()

        self.geometry.height = self._em2px(1.0)
        if self.geometry.height % 2 != 0:
            self.geometry.height += 1

        margin_left = self._em2px(0.4)
        margin_right = self._em2px(0.2)

        self.geometry.center_y = self.geometry.height // 2
        self.geometry.arc_width = self.geometry.height // 2
        self.geometry.text_left = self.geometry.arc_width + margin_left

        self.geometry.button_border_x = self.geometry.text_left - self._em2px(0.1)
        self.geometry.button_center_x = self._em2px(0.4)
        self.geometry.button_center_y = self.geometry.center_y

        button_add_width = self._em2px(0.5)
        if button_add_width % 2 != 0:
            button_add_width += 1

        button_add_height = button_add_width
        self.geometry.button_add_left = (
            self.geometry.button_center_x - button_add_width // 2
        )
        self.geometry.button_add_right = (
            self.geometry.button_center_x + button_add_width // 2
        )
        self.geometry.button_add_top = self.geometry.center_y - button_add_height // 2
        self.geometry.button_add_bottom = (
            self.geometry.center_y + button_add_height // 2
        )

        button_remove_width = self._em2px(0.33)
        button_remove_height = self._em2px(0.35)
        self.geometry.button_remove_left = (
            self.geometry.button_center_x - button_remove_width // 2
        )
        self.geometry.button_remove_right = (
            self.geometry.button_remove_left + button_remove_width
        )
        self.geometry.button_remove_top = (
            self.geometry.center_y - button_remove_height // 2
        )
        self.geometry.button_remove_bottom = (
            self.geometry.center_y + button_remove_height // 2
        )

        self.geometry.font_size = int(
            self._min_font_size
            + self._ratio * (self._max_font_size - self._min_font_size)
        )

        self.geometry.text_width = self._calc_text_size(
            self._label, self.geometry.font_size
        )[0]

        self.geometry.width = (
            self.geometry.arc_width
            + margin_left
            + self.geometry.text_width
            + margin_right
        )

    def setRatio(self, ratio):
        """
        Установить коэффициент, показывающий относительный размер метки.
        Коэффициент должен быть в интервале [0; 1]
        """
        self._ratio = ratio
        self._calc_geometry()

    def mark(self, marked: bool = True):
        self._is_marked = marked

    @property
    def isMarked(self) -> bool:
        return self._is_marked

    def onLeftDown(self, x, y):
        if self._use_buttons and x <= self.geometry.button_border_x:
            self._sendTagEvent(TagRemoveEvent if self._is_marked else TagAddEvent)
        else:
            self._sendTagEvent(TagLeftDownEvent)

    def onRightDown(self, x, y):
        self._sendTagEvent(TagRightDownEvent)

    def onMiddleDown(self, x, y):
        self._sendTagEvent(TagMiddleDownEvent)

    def onLeftUp(self, x, y):
        self._sendTagEvent(TagLeftUpEvent)

    def onRightUp(self, x, y):
        self._sendTagEvent(TagRightUpEvent)

    def onMiddleUp(self, x, y):
        self._sendTagEvent(TagMiddleUpEvent)

    def updateButtonHover(self, x, y):
        self._is_hover_button = x <= self.geometry.button_border_x

    def _sendTagEvent(self, eventType):
        newevent = eventType(text=self._label)
        newevent.ResumePropagation(self._propagationLevel)
        wx.PostEvent(self._parent, newevent)


class _TagPainter:
    def __init__(self, parent: wx.Window, theme: Theme) -> None:
        self._parent = parent
        self._theme = theme
        self._update_theme()

    def _update_theme(self):
        # ToDo: Read colors from Theme
        self._back_color = self._theme.colorBackground

        self._normal_back_color = self._back_color
        self._normal_border_color = self._back_color
        self._normal_font_color = wx.Colour("#34609D")

        self._normal_hover_back_color = wx.Colour("#D6E7FD")
        self._normal_hover_border_color = wx.Colour("#78D8FC")
        self._normal_hover_font_color = wx.Colour("#34609D")
        self._add_button_color = wx.Colour("#577EBF")
        self._hover_add_button_color = wx.Colour("#20518C")

        self._marked_back_color = wx.Colour("#fcde78")
        self._marked_border_color = wx.Colour("#EDB14A")
        self._marked_font_color = wx.Colour("#714b0a")

        self._marked_hover_back_color = wx.Colour("#FFC500")
        self._marked_hover_border_color = wx.Colour("#B5931E")
        self._marked_hover_font_color = wx.Colour("#000000")
        self._remove_button_color = wx.Colour("#B5931E")
        self._hover_remove_button_color = wx.Colour("#8B6D00")

    def draw(self, label: TagLabel2, y_scroll: int, dc: wx.DC, gc: wx.GraphicsContext):
        if not label.isVisible():
            return

        x0 = label.x
        y0 = label.y - y_scroll

        # Draw background
        gc.SetBrush(wx.Brush(self._back_color))
        gc.SetPen(wx.Pen(self._back_color))
        gc.DrawRectangle(x0, y0, label.geometry.width, label.geometry.height)

        # Draw tag
        tag_back_color = self._get_back_color(label)
        tag_border_color = self._get_border_color(label)
        gc.SetBrush(wx.Brush(tag_back_color))
        pen = wx.Pen(tag_border_color, 1)
        pen.SetQuality(wx.PEN_QUALITY_HIGH)
        gc.SetPen(pen)

        path = gc.CreatePath()
        path.MoveToPoint(label.geometry.button_border_x + x0, y0)
        path.AddArc(
            label.geometry.arc_width + x0,
            label.geometry.center_y + y0,
            label.geometry.height // 2,
            math.pi * 1.5,
            math.pi * 0.5,
            clockwise=False,
        )
        path.AddLineToPoint(
            label.geometry.button_border_x + x0, label.geometry.height + y0
        )
        path.AddLineToPoint(label.geometry.width + x0, label.geometry.height + y0)
        path.AddLineToPoint(label.geometry.width + x0, y0)
        path.AddLineToPoint(label.geometry.button_border_x + x0, y0)

        gc.DrawPath(path)

        # Draw text
        text_size = self._calc_text_size(label.label, label.geometry.font_size)
        font_color = self._get_font_color(label)

        font = wx.Font(wx.FontInfo(label.geometry.font_size))
        dc.SetTextForeground(font_color)
        dc.SetFont(font)
        text_x = label.geometry.text_left
        text_y = int((label.geometry.height - text_size[1]) / 2)
        dc.DrawText(label.label, text_x + x0, text_y + y0)

        # Draw the Add / Remove button
        if label.isUseButtons:
            if label.isHovered and not label.isMarked:
                self._draw_add_button(label, gc, x0, y0)
            elif label.isHovered and label.isMarked:
                self._draw_remove_button(label, gc, x0, y0)

    def _calc_text_size(self, text: str, font_size: int) -> Tuple[int, int]:
        with wx.ClientDC(self._parent) as dc:
            font = wx.Font(wx.FontInfo(font_size))
            dc.SetFont(font)
            return dc.GetTextExtent(text)

    def _draw_add_button(
        self, label: TagLabel2, gc: wx.GraphicsContext, x0: int, y0: int
    ):
        line_width = 2
        button_color = (
            self._hover_add_button_color
            if label.isButtonHovered
            else self._add_button_color
        )
        gc.SetBrush(wx.Brush(button_color))
        gc.SetPen(wx.NullPen)

        # Horizontal line
        gc.DrawRectangle(
            label.geometry.button_add_left + x0,
            label.geometry.button_center_y - line_width // 2 + y0,
            label.geometry.button_add_right - label.geometry.button_add_left,
            line_width,
        )

        # Vertical line
        gc.DrawRectangle(
            label.geometry.button_center_x - line_width // 2 + x0,
            label.geometry.button_add_top + y0,
            line_width,
            label.geometry.button_add_bottom - label.geometry.button_add_top,
        )

        border_x = int((label.geometry.button_add_right + label.geometry.text_left) / 2)
        gc.SetPen(wx.Pen(self._normal_hover_border_color))
        gc.DrawLines([(border_x + x0, y0), (border_x + x0, label.geometry.height + y0)])

    def _draw_remove_button(
        self, label: TagLabel2, gc: wx.GraphicsContext, x0: int, y0: int
    ):
        line_width = 2
        button_color = (
            self._hover_remove_button_color
            if label.isButtonHovered
            else self._remove_button_color
        )
        gc.SetPen(wx.Pen(button_color, line_width))

        gc.DrawLines(
            [
                (
                    label.geometry.button_remove_left + x0,
                    label.geometry.button_remove_top + y0,
                ),
                (
                    label.geometry.button_remove_right + x0,
                    label.geometry.button_remove_bottom + y0,
                ),
            ]
        )

        gc.DrawLines(
            [
                (
                    label.geometry.button_remove_left + x0,
                    label.geometry.button_remove_bottom + y0,
                ),
                (
                    label.geometry.button_remove_right + x0,
                    label.geometry.button_remove_top + y0,
                ),
            ]
        )

        border_x = int(
            (label.geometry.button_remove_right + label.geometry.text_left) / 2
        )
        gc.SetPen(wx.Pen(self._marked_hover_border_color))
        gc.DrawLines([(border_x + x0, y0), (border_x + x0, label.geometry.height + y0)])

    def _get_font_color(self, label: TagLabel2) -> wx.Colour:
        if label.isMarked and not label.isHovered:
            return self._marked_font_color

        if label.isMarked and label.isHovered:
            return self._marked_hover_font_color

        if not label.isMarked and label.isHovered:
            return self._normal_hover_font_color

        return self._normal_font_color

    def _get_back_color(self, label: TagLabel2) -> wx.Colour:
        if label.isMarked and not label.isHovered:
            return self._marked_back_color

        if label.isMarked and label.isHovered:
            return self._marked_hover_back_color

        if not label.isMarked and label.isHovered:
            return self._normal_hover_back_color

        return self._normal_back_color

    def _get_border_color(self, label: TagLabel2) -> wx.Colour:
        if label.isMarked and not label.isHovered:
            return self._marked_border_color

        if label.isMarked and label.isHovered:
            return self._marked_hover_border_color

        if not label.isMarked and label.isHovered:
            return self._normal_hover_border_color

        return self._normal_border_color


class TagsCloud(wx.Panel):
    def __init__(
        self,
        parent: wx.Window,
        theme: Theme,
        use_buttons: bool = True,
        min_font_size: int = 8,
        max_font_size: int = 16,
        mode: str = TAGS_CLOUD_MODE_CONTINUOUS,
        enable_tooltips: bool = True,
        enable_active_tags_filter: bool = True,
    ):
        super().__init__(parent)
        self._theme = theme
        self._use_buttons = use_buttons
        self._min_font_size = min_font_size
        self._max_font_size = max_font_size
        self._mode = mode
        self._enable_tooltips = enable_tooltips
        self._enable_active_tags_filter = enable_active_tags_filter
        self._buffer = wx.Bitmap(self.GetClientSize())

        self._scroll_start_time = None
        self._scroll_timeout_musec = 200e3

        # Отступ от края окна
        self._margin = 4

        # Зазор между тегами по горизонтали
        self._gapx = 10

        # Зазор между метками по вертикали
        self._gapy = 4

        # Size of the control before tags layout
        self._oldSize = (-1, -1)

        self._filter = ""
        self._tags: Optional[TagsList] = None
        self._filtered_tags: List[str] = []

        # Ключ - имя метки, значение - контрол, отображающий эту метку
        self._labels: Dict[str, TagLabel2] = {}

        self._prevLabelHovered: Optional[TagLabel2] = None

        self._create_gui()
        self._tag_painter = _TagPainter(self._tags_panel, self._theme)

        self._tags_panel.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftDown)
        self._tags_panel.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightDown)
        self._tags_panel.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleDown)

        self._tags_panel.Bind(wx.EVT_LEFT_UP, handler=self._onLeftUp)
        self._tags_panel.Bind(wx.EVT_RIGHT_UP, handler=self._onRightUp)
        self._tags_panel.Bind(wx.EVT_MIDDLE_UP, handler=self._onMiddleUp)

        self._tags_panel.Bind(wx.EVT_SIZE, self.__onSize)
        self._tags_panel.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self._tags_panel.Bind(wx.EVT_MOTION, handler=self._onMouseMove)
        self._tags_panel.Bind(wx.EVT_LEAVE_WINDOW, handler=self._onMouseLeaveWindow)
        self._tags_panel.Bind(wx.EVT_SCROLLWIN, handler=self._onScroll)
        self._search_ctrl.Bind(wx.EVT_TEXT, handler=self._onSearch)
        self._search_ctrl.Bind(wx.EVT_KEY_DOWN, self._onKeyPressed)
        self._active_tags_flag.Bind(wx.EVT_TOGGLEBUTTON, self._onActiveTagsToggle)

    def _findLabel(self, x, y) -> Optional[TagLabel2]:
        result = None

        for label in self._labels.values():
            if not label.isVisible():
                continue

            label_x_min, label_y_min = label.getPosition()
            label_x_max, label_y_max = label.getPositionMax()
            if (
                y >= label_y_min
                and y <= label_y_max
                and x >= label_x_min
                and x <= label_x_max
            ):
                result = label
                break

            if y < label_y_min:
                break

        return result

    def _getMouseCoord(self, event) -> Tuple[int, int]:
        return (event.GetX(), event.GetY() + self.getScrolledY()[0])

    def _setLabelHover(self, label: TagLabel2, value: bool):
        old_value = label.isHovered
        if old_value != value:
            label.setHover(value)
            self._refreshLabel(label)

    def _markLabel(self, label: TagLabel2, value: bool):
        old_value = label.isMarked
        if old_value != value:
            label.mark(value)
            self._refreshLabel(label)

    def _onScroll(self, event):
        event.Skip()
        # Don't repaint labels during scroll
        self._scroll_start_time = datetime.now()
        if self._prevLabelHovered is not None:
            self._setLabelHover(self._prevLabelHovered, False)
            self._tags_panel.UnsetToolTip()
            self._prevLabelHovered = None

    def _onMouseLeaveWindow(self, event):
        if self._prevLabelHovered is not None:
            self._setLabelHover(self._prevLabelHovered, False)

    def _onMouseMove(self, event):
        # Don't repaint labels during scroll
        if self._scroll_start_time is not None:
            delta = datetime.now() - self._scroll_start_time
            if delta.microseconds >= self._scroll_timeout_musec:
                self._scroll_start_time = None
            else:
                return

        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)

        if self._prevLabelHovered is not None and label is not self._prevLabelHovered:
            self._tags_panel.UnsetToolTip()
            self._setLabelHover(self._prevLabelHovered, False)

        if label is not None and label is not self._prevLabelHovered:
            self._setLabelHover(label, True)
            if self._enable_tooltips:
                assert self._tags is not None
                tooltip = _("Number of notes: {}").format(
                    len(self._tags[label.getLabel()])
                )
                self._tags_panel.SetToolTip(tooltip)

        self._prevLabelHovered = label

        # Mouse over button inside tag?
        if label is not None:
            label_x, label_y = label.getPosition()
            old_button_hover = label.isButtonHovered
            label.updateButtonHover(x - label_x, y - label_y)
            if label.isButtonHovered != old_button_hover:
                self._refreshLabel(label)

    def _callTagEvent(self, event, method_name):
        event.Skip()
        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)
        if label is not None:
            label_x, label_y = label.getPosition()
            method = getattr(label, method_name)
            method(x - label_x, y - label_y)

    def _onLeftDown(self, event):
        self._callTagEvent(event, "onLeftDown")

    def _onLeftUp(self, event):
        self._callTagEvent(event, "onLeftUp")

    def _onRightDown(self, event):
        self._callTagEvent(event, "onRightDown")

    def _onRightUp(self, event):
        self._callTagEvent(event, "onRightUp")

    def _onMiddleDown(self, event):
        self._callTagEvent(event, "onMiddleDown")

    def _onMiddleUp(self, event):
        self._callTagEvent(event, "onMiddleUp")

    def getScrolledY(self) -> Tuple[int, int]:
        ymin = (
            self._tags_panel.GetScrollPos(wx.VERTICAL)
            * self._tags_panel.GetScrollPixelsPerUnit()[1]
        )
        ymax = ymin + self._tags_panel.GetClientSize()[1]
        return (ymin, ymax)

    def _refreshLabel(self, label: TagLabel2):
        y_min = self.getScrolledY()[0]
        left = label.x
        top = label.y - y_min
        width = label.geometry.width + 1
        height = label.geometry.height + 1
        self._tags_panel.Refresh(rect=wx.Rect(left, top, width, height))

    def _repaintLabels(self, label_names: Iterable, dc: wx.DC, gc: wx.GraphicsContext):
        y_min, y_max = self.getScrolledY()

        for label_name in label_names:
            label = self._labels[label_name]
            label_y_min = label.getPosition()[1]
            label_y_max = label.getPositionMax()[1]
            if label_y_min <= y_max and label_y_max >= y_min:
                self._tag_painter.draw(label, y_min, dc, gc)

            if label_y_min > y_max:
                break

    def _onPaint(self, event):
        with wx.BufferedPaintDC(self._tags_panel, self._buffer) as dc:
            gc = wx.GraphicsContext.Create(dc)
            back_color = self._theme.colorBackground
            gc.SetBrush(wx.Brush(back_color))
            gc.SetPen(wx.Pen(back_color))
            width, height = self._tags_panel.GetClientSize()
            gc.DrawRectangle(0, 0, width, height)
            self._repaintLabels(self._filtered_tags, dc, gc)

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._min_font_size = min_font_size
        self._max_font_size = max_font_size

        for tag_label in self._labels.values():
            tag_label.setFontSize(min_font_size, max_font_size)

        self._layoutTags()

    def setMode(self, mode):
        self._mode = mode
        self._layoutTags()

    def _create_gui(self):
        self.SetMinSize((150, 150))
        self._main_sizer = wx.FlexGridSizer(cols=1)
        self._main_sizer.AddGrowableCol(0)
        self._main_sizer.AddGrowableRow(1)

        self._tags_panel = wx.ScrolledCanvas(self)
        self._tags_panel.SetScrollRate(0, 0)
        self._tags_panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self._search_ctrl = wx.SearchCtrl(self)
        icon_size = self._theme.get(Theme.SECTION_GENERAL, Theme.BUTTONS_ICON_SIZE)
        tagBitmap = readImage(getBuiltinImagePath("tag.svg"), icon_size, icon_size)
        self._active_tags_flag = wx.BitmapToggleButton(self, label=tagBitmap)
        self._active_tags_flag.SetToolTip(_("Applied tags only"))
        self._active_tags_flag.Show(self._enable_active_tags_filter)

        filter_sizer = wx.FlexGridSizer(cols=2)
        filter_sizer.AddGrowableCol(0)
        filter_sizer.AddGrowableRow(0)

        filter_sizer.Add(self._search_ctrl, flag=wx.EXPAND)
        filter_sizer.Add(self._active_tags_flag, flag=wx.ALIGN_RIGHT | wx.EXPAND)

        self._main_sizer.Add(filter_sizer, flag=wx.EXPAND)
        self._main_sizer.Add(self._tags_panel, flag=wx.EXPAND)

        self.SetSizer(self._main_sizer)

    def __onSize(self, event):
        newSize = self.GetClientSize()
        if self._oldSize != newSize and newSize.Width > 0 and newSize.Height > 0:
            self._buffer = wx.Bitmap(newSize)
            self.__moveLabels()
            self._oldSize = newSize

    def _onSearch(self, event):
        self._updateFilter()

    def _onKeyPressed(self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self._search_ctrl.SetValue("")

        event.Skip()

    def _is_active_only(self):
        return self._active_tags_flag.GetValue()

    def _onActiveTagsToggle(self, event):
        self._updateFilter()

    def _updateFilter(self):
        self.setFilter(self._search_ctrl.GetValue(), self._is_active_only())

    def setTags(self, taglist: TagsList):
        """
        Добавить теги в облако
        """
        self.Freeze()
        oldy = self._tags_panel.GetScrollPos(wx.VERTICAL)
        self.clear()

        self._tags = taglist
        self._create_tag_labels()

        active_only = self._active_tags_flag.GetValue()
        self._filtered_tags = (
            self._filter_tags(self._tags.tags, active_only)
            if self._tags is not None
            else []
        )
        self._filter_tag_labels()
        self._tags_panel.Scroll(-1, oldy)
        self._prevLabelHovered = None
        self.Thaw()
        self._tags_panel.Refresh()

    def setFilter(self, tags_filter: str, active_only: bool = False):
        self._filter = tags_filter

        if self._tags is None:
            return

        self._filtered_tags = (
            self._filter_tags(self._tags.tags, active_only)
            if self._tags is not None
            else []
        )
        self._filter_tag_labels()

    def enableTooltips(self, enable: bool = True):
        if enable != self._enable_tooltips:
            self._enable_tooltips = enable
            if not enable:
                self._tags_panel.UnsetToolTip()

    def _create_tag_labels(self):
        if self._tags is None:
            return

        for tag in self._tags:
            newlabel = TagLabel2(
                self._tags_panel,
                tag,
                self._use_buttons,
                self._min_font_size,
                self._max_font_size,
            )

            self._labels[tag] = newlabel

    def _filter_tag_labels(self):
        if self._tags is None:
            return

        for tag_name in self._tags:
            label = self._labels[tag_name]
            label.Show(tag_name in self._filtered_tags)

        self._layoutTags()

    def _filter_tags(self, tags: List[str], active_only: bool) -> List[str]:
        return list(
            filter(
                lambda tag_name: self._filter.lower() in tag_name.lower()
                and (not active_only or self.isMarked(tag_name)),
                tags,
            )
        )

    def mark(self, tag: str, marked: bool = True):
        """
        Выделить метку
        """
        if tag.lower().strip() in self._labels.keys():
            label = self._labels[tag.lower().strip()]
            self._markLabel(label, marked)
            if self._is_active_only():
                self._updateFilter()

    def mark_list(self, tags: Collection[str], marked: bool = True):
        for tag in tags:
            if tag.lower().strip() in self._labels.keys():
                label = self._labels[tag.lower().strip()]
                self._markLabel(label, marked)

        if self._is_active_only():
            self._updateFilter()

        self._tags_panel.Refresh()

    def clearMarks(self):
        """
        Убрать все выделения с меток
        """
        for label in self._labels.values():
            self._markLabel(label, False)

        if self._is_active_only():
            self._updateFilter()

    def isMarked(self, tag):
        return self._labels[tag].isMarked

    def clear(self):
        self._labels = {}
        self._tags = None
        self._filtered_tags = []

    def __getMaxCount(self) -> int:
        count = 0
        if self._tags is None:
            return count

        for tag in self._tags:
            if len(self._tags[tag]) > count:
                count = len(self._tags[tag])

        return count

    def __calcSizeRatio(self, count):
        assert self._tags is not None

        maxcount = self.__getMaxCount()
        ratio = 1

        if maxcount != 0:
            ratio = float(count) / maxcount

        return ratio

    def __setSizeLabels(self):
        if self._tags is None:
            return

        for tagname in self._filtered_tags:
            count = len(self._tags[tagname])
            ratio = self.__calcSizeRatio(count)

            label = self._labels[tagname]
            label.setRatio(ratio)

    def _layoutTags(self):
        """
        Расположение тегов в окне
        """
        if self._tags is None:
            return

        self.__setSizeLabels()
        self.__moveLabels()

    def __moveLabels(self):
        if self._tags is None or len(self._tags) == 0:
            return

        assert len(self._labels) != 0

        # Хак из-за разного поведения полос прокрутки в винде и линуксе
        if os.name != "nt":
            self._tags_panel.SetScrollbars(0, 0, 0, 0)

        if self._mode == TAGS_CLOUD_MODE_LIST:
            self.__moveLabelsAsList()
        else:
            self.__moveLabelsContinuous()

        self._tags_panel.Refresh()

    def _getScrollStepY(self) -> int:
        return list(self._labels.values())[0].getSize()[1] + self._gapy

    def __moveLabelsAsList(self):
        stepy = self._getScrollStepY()

        for line, tagname in enumerate(self._filtered_tags):
            label = self._labels[tagname]
            label.Move(self._margin, self._margin + line * stepy)

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, len(self._filtered_tags))

    def __moveLabelsContinuous(self):
        stepy = list(self._labels.values())[0].getSize()[1] + self._gapy

        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self._margin
        currenty = self._margin

        linesCount = 1

        maxwidth = self._tags_panel.GetClientSize()[0] - self._margin * 2

        for tagname in self._filtered_tags:
            label = self._labels[tagname]

            newRightBorder = currentx + label.getSize()[0]

            if newRightBorder > maxwidth and len(currentLine) != 0:
                currentx = self._margin
                currenty += stepy

                currentLine = []
                linesCount += 1

            label.Move(currentx, currenty)

            currentLine.append(label)
            currentx += label.getSize()[0] + self._gapx

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, linesCount)

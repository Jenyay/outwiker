from typing import Optional, Tuple

import wx
import wx.lib.newevent

TagLeftDownEvent, EVT_TAG_LEFT_DOWN = wx.lib.newevent.NewEvent()
TagLeftUpEvent, EVT_TAG_LEFT_UP = wx.lib.newevent.NewEvent()

TagRightDownEvent, EVT_TAG_RIGHT_DOWN = wx.lib.newevent.NewEvent()
TagRightUpEvent, EVT_TAG_RIGHT_UP = wx.lib.newevent.NewEvent()

TagMiddleDownEvent, EVT_TAG_MIDDLE_DOWN = wx.lib.newevent.NewEvent()
TagMiddleUpEvent, EVT_TAG_MIDDLE_UP = wx.lib.newevent.NewEvent()

TagAddEvent, EVT_TAG_ADD = wx.lib.newevent.NewEvent()
TagRemoveEvent, EVT_TAG_REMOVE = wx.lib.newevent.NewEvent()


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
        back_color: Optional[wx.Colour] = None
    ):
        self._parent = parent
        self._label = label
        self._use_buttons = use_buttons
        self._is_marked = False
        self._is_hover = False
        self._is_hover_button = False

        self._x = x
        self._y = y
        self._width = 0
        self._height = 0
        self._visible = True
        self._paint_x = None
        self._paint_y = None

        self._propagationLevel = 10
        self._ratio = 1.0

        self._back_color = wx.Colour("#FFFFFF") if back_color is None else back_color

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

        self.setFontSize(min_font_size, max_font_size)

    def setBackColor(self, color: wx.Colour):
        self._back_color = color
        self._normal_back_color = self._back_color
        self._normal_border_color = self._back_color

    def isHover(self) -> bool:
        return self._is_hover

    def setHover(self, value: bool):
        old_value = self._is_hover
        self._is_hover = value
        if value != old_value:
            self.Refresh()

    def isVisible(self) -> bool:
        return self._visible

    def Move(self, x: int, y: int):
        self._x = x
        self._y = y

    def getSize(self) -> Tuple[int, int]:
        return (self._width, self._height)

    def getPosition(self) -> Tuple[int, int]:
        return (self._x, self._y)

    def getPositionMax(self) -> Tuple[int, int]:
        return (self._x + self._width, self._y + self._height)

    def Show(self, visible=True):
        self._visible = visible

    def getLabel(self) -> str:
        return self._label

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._min_font_size = min(min_font_size, max_font_size)
        self._max_font_size = max(min_font_size, max_font_size)
        self._calc_sizes()

    def _calc_em(self) -> int:
        return self._calc_text_size("Q", self._max_font_size)[1]

    def _calc_text_size(self, text: str, font_size: int) -> Tuple[int, int]:
        with wx.ClientDC(self._parent) as dc:
            font = wx.Font(wx.FontInfo(font_size))
            dc.SetFont(font)
            return dc.GetTextExtent(text)

    def _em2px(self, em: float) -> int:
        return int(em * self._em)

    def _calc_sizes(self):
        self._em = self._calc_em()

        self._height = self._em2px(1.0)
        if self._height % 2 == 0:
            self._height += 1
        self._margin_left = self._em2px(0.4)
        self._margin_right = self._em2px(0.2)

        self._center_y = self._height // 2
        self._arc_width = self._height // 2
        self._text_left = self._arc_width + self._margin_left

        self._button_border_x = self._text_left - self._em2px(0.1)
        self._button_center_x = self._em2px(0.4)
        self._button_center_y = self._center_y

        self._button_add_width = self._em2px(0.5)
        self._button_add_height = self._em2px(0.5)
        self._button_add_left = int(self._button_center_x - self._button_add_width / 2)
        self._button_add_right = self._button_add_left + self._button_add_width
        self._button_add_top = self._center_y - int(self._button_add_height / 2)
        self._button_add_bottom = self._center_y + int(self._button_add_height / 2)

        self._button_remove_width = self._em2px(0.33)
        self._button_remove_height = self._em2px(0.35)
        self._button_remove_left = int(
            self._button_center_x - self._button_remove_width / 2
        )
        self._button_remove_right = self._button_remove_left + self._button_remove_width
        self._button_remove_top = self._center_y - int(self._button_remove_height / 2)
        self._button_remove_bottom = self._center_y + int(
            self._button_remove_height / 2
        )

        self._font_size = int(
            self._min_font_size
            + self._ratio * (self._max_font_size - self._min_font_size)
        )

        self._text_width = self._calc_text_size(self._label, self._font_size)[0]

        self._width = (
            self._arc_width + self._margin_left + self._text_width + self._margin_right
        )

    def _get_current_font(self):
        return wx.Font(wx.FontInfo(self._font_size))

    def setRatio(self, ratio):
        """
        Установить коэффициент, показывающий относительный размер метки.
        Коэффициент должен быть в интервале [0; 1]
        """
        self._ratio = ratio
        self._calc_sizes()

    def mark(self, marked: bool = True):
        self._is_marked = marked
        self.Refresh()

    @property
    def isMarked(self) -> bool:
        return self._is_marked

    @property
    def isUsedButtons(self) -> bool:
        return self._use_buttons

    @isUsedButtons.setter
    def isUsedButtons(self, value):
        old_value = self._use_buttons
        self._use_buttons = value
        if old_value != value:
            self.Refresh()

    def Refresh(self):
        if self._paint_x is not None and self._paint_y is not None:
            with wx.ClientDC(self._parent) as dc:
                self.onPaint(dc, self._paint_x, self._paint_y)

    def onPaint(self, dc, x0, y0):
        if not self._visible:
            return

        self._paint_x = x0
        self._paint_y = y0
        dc.SetDeviceOrigin(x0, y0)

        # Draw background
        dc.SetBrush(wx.Brush(self._back_color))
        dc.SetPen(wx.Pen(self._back_color))
        dc.DrawRectangle(0, 0, self._width, self._height)

        # Draw tag
        tag_back_color = self._get_back_color()
        tag_border_color = self._get_border_color()
        dc.SetBrush(wx.Brush(tag_back_color))
        dc.SetPen(wx.Pen(tag_back_color))
        dc.DrawRectangle(
            self._button_border_x, 0, self._width - self._button_border_x - 1, self._height - 1
        )
        dc.SetPen(wx.Pen(tag_border_color, 1))
        dc.DrawLineList(
            [
                (self._button_border_x, 0, self._width - 1, 0),
                (self._width - 1, 0, self._width - 1, self._height - 1),
                (self._button_border_x, self._height - 1, self._width - 1, self._height - 1),
            ]
        )

        # Draw the Add / Remove button background and border
        button_back_color = self._get_button_back_color()
        button_border_color = self._get_button_border_color()
        dc.SetBrush(wx.Brush(button_back_color))
        dc.SetPen(wx.Pen(button_back_color))
        # dc.DrawEllipse(0, 0, self._height, self._height - 1)
        dc.DrawRectangle(
            self._arc_width, 0, self._button_border_x - self._arc_width, self._height - 1
        )
        dc.SetPen(wx.Pen(button_border_color, 1))
        dc.DrawEllipticArc(0, 0, self._height, self._height - 1, 90, 270)
        dc.DrawLineList(
            [
                (self._arc_width, 0, self._button_border_x, 0),
                (self._arc_width, self._height - 1, self._button_border_x, self._height - 1),
            ]
        )

        # Draw text
        text_size = self._calc_text_size(self._label, self._font_size)
        font_color = self._get_font_color()
        font = self._get_current_font()
        dc.SetTextForeground(font_color)
        dc.SetFont(font)
        text_x = self._text_left
        text_y = int((self._height - text_size[1]) / 2)
        dc.DrawText(self._label, text_x, text_y)

        # Draw the Add / Remove button
        if self._use_buttons:
            if self._is_hover and not self._is_marked:
                self._draw_add_button(dc)
            elif self._is_hover and self._is_marked:
                self._draw_remove_button(dc)

    def _draw_add_button(self, dc: wx.DC):
        width = 2
        button_color = self._hover_add_button_color if self._is_hover_button else self._add_button_color
        dc.SetBrush(wx.Brush(button_color))
        dc.SetPen(wx.Pen(button_color))
        dc.DrawRectangle(
            self._button_add_left,
            int(self._button_center_y - width / 2),
            self._button_add_width + 1,
            width,
        )

        dc.DrawRectangle(
            int(self._button_center_x - width / 2),
            self._button_add_top - 1,
            width,
            self._button_add_height + 1,
        )

        border_x = int((self._button_add_right + self._text_left) / 2)
        dc.SetPen(wx.Pen(self._normal_hover_border_color))
        dc.DrawLine(border_x, 0, border_x, self._height)

    def _draw_remove_button(self, dc: wx.DC):
        width = 2
        button_color = self._hover_remove_button_color if self._is_hover_button else self._remove_button_color
        dc.SetPen(wx.Pen(button_color, width))
        dc.DrawLineList(
            [
                (
                    self._button_remove_left,
                    self._button_remove_top,
                    self._button_remove_right,
                    self._button_remove_bottom,
                ),
                (
                    self._button_remove_left,
                    self._button_remove_bottom,
                    self._button_remove_right,
                    self._button_remove_top,
                ),
            ]
        )

        border_x = int((self._button_remove_right + self._text_left) / 2)
        dc.SetPen(wx.Pen(self._marked_hover_border_color))
        dc.DrawLine(border_x, 0, border_x, self._height)

    def onLeftDown(self, x, y):
        if self._use_buttons and x <= self._button_border_x:
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

    def onMouseMove(self, x, y):
        new_is_hover_button = x <= self._button_border_x
        if new_is_hover_button != self._is_hover_button:
            self._is_hover_button = new_is_hover_button
            self.Refresh()

    def _sendTagEvent(self, eventType):
        newevent = eventType(text=self._label)
        newevent.ResumePropagation(self._propagationLevel)
        wx.PostEvent(self._parent, newevent)

    def _get_font_color(self) -> wx.Colour:
        if self._is_marked and not self._is_hover:
            return self._marked_font_color

        if self._is_marked and self._is_hover:
            return self._marked_hover_font_color

        if not self._is_marked and self._is_hover:
            return self._normal_hover_font_color

        return self._normal_font_color

    def _get_back_color(self) -> wx.Colour:
        if self._is_marked and not self._is_hover:
            return self._marked_back_color

        if self._is_marked and self._is_hover:
            return self._marked_hover_back_color

        if not self._is_marked and self._is_hover:
            return self._normal_hover_back_color

        return self._normal_back_color

    def _get_border_color(self) -> wx.Colour:
        if self._is_marked and not self._is_hover:
            return self._marked_border_color

        if self._is_marked and self._is_hover:
            return self._marked_hover_border_color

        if not self._is_marked and self._is_hover:
            return self._normal_hover_border_color

        return self._normal_border_color

    def _get_button_back_color(self) -> wx.Colour:
        if self._is_marked and not self._is_hover:
            return self._marked_back_color

        if self._is_marked and self._is_hover:
            return self._marked_hover_back_color

        if not self._is_marked and self._is_hover:
            return self._normal_hover_back_color

        return self._normal_back_color

    def _get_button_border_color(self) -> wx.Colour:
        if self._is_marked and not self._is_hover:
            return self._marked_border_color

        if self._is_marked and self._is_hover:
            return self._marked_hover_border_color

        if not self._is_marked and self._is_hover:
            return self._normal_hover_border_color

        return self._normal_border_color

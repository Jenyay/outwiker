from typing import Tuple

import wx
import wx.lib.newevent

TagLeftClickEvent, EVT_TAG_LEFT_CLICK = wx.lib.newevent.NewEvent()
TagRightClickEvent, EVT_TAG_RIGHT_CLICK = wx.lib.newevent.NewEvent()
TagMiddleClickEvent, EVT_TAG_MIDDLE_CLICK = wx.lib.newevent.NewEvent()
TagAddEvent, EVT_TAG_ADD = wx.lib.newevent.NewEvent()
TagRemoveEvent, EVT_TAG_REMOVE = wx.lib.newevent.NewEvent()


class TagLabel2(wx.Control):
    def __init__(self, parent, label, use_buttons: bool = True):
        super().__init__(
            parent,
            style=wx.BORDER_NONE)

        self._label = label
        self._use_buttons = use_buttons
        self._is_marked = False
        self._is_hover = False
        self._is_hover_button = False

        self._propagationLevel = 10
        self._min_font_size = 8
        self._max_font_size = 16
        self._ratio = 1.0
        self._em = self._calc_em()

        self._back_color = wx.Colour("#FFFFFF")

        self._normal_back_color = wx.Colour("#FFFFFF")
        self._normal_border_color = wx.Colour("#FFFFFF")
        self._normal_font_color = wx.Colour("#34609D")

        self._normal_hover_back_color = wx.Colour("#D6E7FD")
        self._normal_hover_border_color = wx.Colour("#78D8FC")
        self._normal_hover_font_color = wx.Colour("#34609D")
        self._add_button_color = wx.Colour("#34609D")

        self._marked_back_color = wx.Colour("#fcde78")
        self._marked_border_color = wx.Colour("#EDB14A")
        self._marked_font_color = wx.Colour("#714b0a")

        self._marked_hover_back_color = wx.Colour("#FFC500")
        self._marked_hover_border_color = wx.Colour("#B5931E")
        self._marked_hover_font_color = wx.Colour("#000000")
        self._remove_button_color = wx.Colour("#B5931E")

        self._height = self._em2px(1.0)
        self._margin_left = self._em2px(0.4)
        self._margin_right = self._em2px(0.2)

        self._center_y = int(self._height / 2)
        self._arc_width = int(self._height / 2)
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
        self._button_remove_left = int(self._button_center_x - self._button_remove_width / 2)
        self._button_remove_right = self._button_remove_left + self._button_remove_width
        self._button_remove_top = self._center_y - int(self._button_remove_height / 2)
        self._button_remove_bottom = self._center_y + int(self._button_remove_height / 2)

        self._font_size = self._max_font_size
        self._text_width = 0
        self._width = 0
        self._calc_sizes()

        self.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, handler=self._onMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, handler=self._onMouseLeave)
        self.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftMouseClick)
        self.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightMouseClick)
        self.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleMouseClick)

    def _calc_em(self) -> int:
        return self._calc_text_size("Q", self._max_font_size)[1]

    def _calc_text_size(self, text: str, font_size: int) -> Tuple[int, int]:
        with wx.ClientDC(self) as dc:
            font = wx.Font(wx.FontInfo(font_size))
            dc.SetFont(font)
            return dc.GetTextExtent(text)

    def _em2px(self, em: float) -> int:
        return int(em * self._em)

    def _calc_sizes(self):
        self._font_size = int(self._min_font_size + self._ratio *
                              (self._max_font_size - self._min_font_size))
        self._text_width = self._calc_text_size(self._label, self._font_size)[0]
        self._width = self._arc_width + self._margin_left + self._text_width + self._margin_right
        self.SetClientSize(self._width, self._height)

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

    def _onPaint(self, event):
        dc = wx.PaintDC(self)

        # Draw background
        dc.SetBrush(wx.Brush(self._back_color))
        dc.SetPen(wx.Pen(self._back_color))
        dc.DrawRectangle(0, 0, self._width, self._height)

        # Draw tag
        tag_back_color = self._get_back_color()
        tag_border_color = self._get_border_color()
        dc.SetBrush(wx.Brush(tag_back_color))
        dc.SetPen(wx.Pen(tag_back_color))
        dc.DrawRectangle(self._arc_width, 0, self._width - self._arc_width - 1, self._height - 1)
        dc.DrawEllipse(0, 0, self._height, self._height)
        dc.SetPen(wx.Pen(tag_border_color, 1))
        dc.DrawLineList([
            (self._arc_width, 0, self._width - 1, 0),
            (self._width - 1, 0, self._width - 1, self._height - 1),
            (self._arc_width, self._height - 1, self._width - 1, self._height - 1),
            ])
        dc.DrawEllipticArc(0, 0, self._height, self._height - 1, 90, 270)

        # Draw text
        text_size = self._calc_text_size(self._label, self._font_size)
        font_color = self._get_font_color()
        font = self._get_current_font()
        dc.SetTextForeground(font_color)
        dc.SetFont(font)
        text_x = self._text_left
        text_y = int((self._height - text_size[1]) / 2)
        dc.DrawText(self._label, text_x, text_y)

        # Draw button
        if self._use_buttons:
            if self._is_hover and not self._is_marked:
                self._draw_add_button(dc)
            elif self._is_hover and self._is_marked:
                self._draw_remove_button(dc)

    def _draw_add_button(self, dc: wx.DC):
        width = 2
        dc.SetBrush(wx.Brush(self._add_button_color))
        dc.SetPen(wx.Pen(self._add_button_color))
        dc.DrawRectangle(self._button_add_left,
                         int(self._button_center_y - width / 2),
                         self._button_add_width,
                         width)

        dc.DrawRectangle(int(self._button_center_x - width / 2),
                         self._button_add_top,
                         width,
                         self._button_add_height)

        border_x = int((self._button_add_right + self._text_left) / 2)
        dc.SetPen(wx.Pen(self._normal_hover_border_color))
        dc.DrawLine(border_x, 0, border_x, self._height)

    def _draw_remove_button(self, dc: wx.DC):
        width = 2
        dc.SetPen(wx.Pen(self._remove_button_color, width))
        dc.DrawLineList([
            (self._button_remove_left, self._button_remove_top, self._button_remove_right, self._button_remove_bottom),
            (self._button_remove_left, self._button_remove_bottom, self._button_remove_right, self._button_remove_top),
            ])

        border_x = int((self._button_remove_right + self._text_left) / 2)
        dc.SetPen(wx.Pen(self._marked_hover_border_color))
        dc.DrawLine(border_x, 0, border_x, self._height)

    def _onMouseEnter(self, event):
        self._is_hover = True
        self.Refresh()

    def _onMouseLeave(self, event):
        self._is_hover = False
        self.Refresh()

    def _onLeftMouseClick(self, event):
        x = event.GetX()
        if self._use_buttons and x <= self._button_border_x:
            self._sendTagEvent(TagRemoveEvent if self._is_marked else TagAddEvent)
        else:
            self._sendTagEvent(TagLeftClickEvent)

    def _onRightMouseClick(self, event):
        self._sendTagEvent(TagRightClickEvent)

    def _onMiddleMouseClick(self, event):
        self._sendTagEvent(TagMiddleClickEvent)

    def _sendTagEvent(self, eventType):
        newevent = eventType(text=self._label)
        newevent.ResumePropagation(self._propagationLevel)
        wx.PostEvent(self.GetParent(), newevent)

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

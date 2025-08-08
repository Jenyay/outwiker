import math
from typing import List, Optional

from outwiker.gui.theme import Theme
import wx
import wx.lib.newevent

from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.core.application import Application
from outwiker.core.history import History


TabsCtrlPageChangedEvent, EVT_TABSCTRL_PAGE_CHANGED = wx.lib.newevent.NewEvent()

TAB_STATE_NORMAL = 0
TAB_STATE_HOVER = 1
TAB_STATE_SELECTED = 2


class TabsCtrl(wx.Control):
    def __init__(self, parent: wx.Window, application: Application, theme: Theme):
        super().__init__(parent)
        self._application = application
        self._theme = theme

        self._lbutton_downed_tab: Optional[int] = None
        self._lbutton_downed_close_button: Optional[int] = None
        self._current_rows_count = 0

        self._tabs_collection: List[TabInfo] = []
        self._current_page_index: Optional[int] = None

        self._geometry = TabsGeometryCalculator()
        self._tab_render = TabRender(self._theme)

        self.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW, handler=self._onMouseLeaveWindow)
        self.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftButtonDown)
        self.Bind(wx.EVT_LEFT_UP, handler=self._onLeftButtonUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleButtonDown)
        self.Bind(wx.EVT_SIZE, handler=self._onSize)

        self._layout()

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)

    def _layout(self):
        text_height = 14
        self._geometry.calc(self._tabs_collection, self.GetClientSize()[0], text_height)
        self.SetMinSize((-1, self._geometry.full_height))
        rows_count = self._geometry.rows_count

        if rows_count != self._current_rows_count:
            self._current_rows_count = rows_count
            self.GetParent().Layout()

    def _onSize(self, event: wx.SizeEvent) -> None:
        self._layout()
        self.Refresh(False)

    def _onMouseLeaveWindow(self, event: wx.MouseEvent) -> None:
        self._lbutton_downed_close_button = None
        self._lbutton_downed_tab = None

    def _onLeftButtonDown(self, event: wx.MouseEvent) -> None:
        self._lbutton_downed_close_button = None
        self._lbutton_downed_tab = None

        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        self._lbutton_downed_tab = tab_number

    def _onLeftButtonUp(self, event: wx.MouseEvent) -> None:
        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        if (
            tab_number is not None
            and tab_number == self._lbutton_downed_tab
            and tab_number != self._current_page_index
        ):
            self.SetSelection(tab_number)

        self._lbutton_downed_close_button = None
        self._lbutton_downed_tab = None

    def _onMiddleButtonDown(self, event: wx.MouseEvent) -> None:
        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        if tab_number is not None:
            self.DeletePage(tab_number)

    def _find_tab_by_coord(self, x: int, y: int) -> Optional[int]:
        if self._geometry.geometry is None:
            return None

        for n, tab in enumerate(self._geometry.geometry):
            if x >= tab.left and x <= tab.right and y >= tab.top and y <= tab.bottom:
                return n

        return None

    def _updateHistoryButtons(self):
        """
        Активировать или дезактивировать кнопки Вперед / Назад
        """
        history = self._getCurrentHistory()
        if history is None:
            self._application.actionController.enableTools(
                HistoryBackAction.stringId, False
            )
            self._application.actionController.enableTools(
                HistoryForwardAction.stringId, False
            )
        else:
            self._application.actionController.enableTools(
                HistoryBackAction.stringId, history.backLength != 0
            )
            self._application.actionController.enableTools(
                HistoryForwardAction.stringId, history.forwardLength != 0
            )

    def AddPage(self, title, page):
        self._tabs_collection.append(TabInfo(page, title))
        if len(self._tabs_collection) == 1:
            self.SetSelection(0)

        self._layout()
        # blankWindow = TabInfo(page)
        # self._tabs.AddPage(blankWindow, title)

    def InsertPage(self, index, title, page, select):
        self._tabs_collection.insert(index, TabInfo(page, title))
        if select:
            self.SetSelection(index)

        self._layout()
        # self._updateHistoryButtons()

    def Clear(self):
        self.SetSelection(None)
        self._tabs_collection.clear()
        self._layout()
        # self._updateHistoryButtons()

    def GetPageText(self, index):
        return self._tabs_collection[index].title

    def RenameCurrentTab(self, title):
        page_index = self.GetSelection()
        if page_index is not None:
            self.RenameTab(page_index, title)

        self._layout()

    def RenameTab(self, index, title):
        self._tabs_collection[index].title = title
        self._layout()

    def GetPage(self, index: Optional[int]):
        return self._tabs_collection[index].page if index is not None else None

    def SetCurrentPage(self, page, title):
        page_index = self.GetSelection()
        if page_index is not None:
            self._tabs_collection[page_index].page = page
            self._tabs_collection[page_index].title = title
            assert self._geometry.geometry is not None
            tab = self._geometry.geometry[page_index]
            self.Refresh(False, wx.Rect(tab.left, tab.top, tab.width, tab.height))

        self._updateHistoryButtons()

    def _getCurrentHistory(self):
        """
        Возвращает класс истории для текущей вкладки
        """
        page_index = self.GetSelection()

        if page_index is not None:
            return self._tabs_collection[page_index].history

    def GetSelection(self) -> Optional[int]:
        return self._current_page_index

    def GetPages(self):
        return [self.GetPage(index) for index in range(self.GetPageCount())]

    def GetPageCount(self):
        return len(self._tabs_collection)

    def SetSelection(self, index: Optional[int]):
        self._current_page_index = index
        self._updateHistoryButtons()
        page = self._tabs_collection[index].page if index is not None else None
        event = TabsCtrlPageChangedEvent(selection=index, page=page)
        wx.PostEvent(self, event)
        wx.SafeYield()

    def DeletePage(self, index):
        assert self._current_page_index is not None
        old_selection = self._current_page_index
        is_delete_selection = index == old_selection
        is_delete_before = index < old_selection

        if index < len(self._tabs_collection):
            del self._tabs_collection[index]

        if is_delete_before:
            self._current_page_index -= 1
            self._layout()
            return

        if is_delete_selection:
            new_count = len(self._tabs_collection)
            new_index = old_selection
            if new_index >= new_count:
                new_index = new_count - 1

            if new_count == 0:
                new_index = None

            self.SetSelection(new_index)
        self._layout()

    def NextPage(self):
        count = len(self._tabs_collection)
        old_selection = self._current_page_index
        if old_selection is None and count != 0:
            self.SetSelection(0)
            return

        if old_selection is not None and old_selection < count - 1:
            self.SetSelection(old_selection + 1)

        # After the last page switch to the first page
        if old_selection is not None and old_selection == count - 1 and count > 1:
            self.SetSelection(0)

    def PreviousPage(self):
        count = len(self._tabs_collection)
        old_selection = self._current_page_index
        if old_selection is None and count != 0:
            self.SetSelection(0)
            return

        if old_selection is not None and old_selection > 0:
            self.SetSelection(old_selection - 1)

        # After the first page switch to the last page
        if old_selection is not None and old_selection == 0 and count > 1:
            self.SetSelection(count - 1)

    def HistoryBack(self):
        page = self._getCurrentHistory().back()
        self._application.selectedPage = page
        self._updateHistoryButtons()

    def HistoryForward(self):
        page = self._getCurrentHistory().forward()
        self._application.selectedPage = page
        self._updateHistoryButtons()

    def _onPaint(self, event: wx.PaintEvent):
        """
        Обработчик события перерисовки вкладок
        """
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self._theme.colorBackground))
        dc.Clear()

        if self._geometry.geometry is None:
            return

        for n, tab in enumerate(self._geometry.geometry):
            state = (
                TAB_STATE_SELECTED
                if n == self._current_page_index
                else TAB_STATE_NORMAL
            )
            self._tab_render.paint(dc, tab, state)

        event.Skip()


class TabInfo:
    """
    Класс окна, хранимого внутри владки с дополнительной информацией
    (текущая страница, история)
    """

    def __init__(self, page, title: str):
        self._title = title
        self._history = History()
        self._history.goto(page)

    @property
    def page(self):
        return self._history.currentPage

    @page.setter
    def page(self, page):
        self._history.goto(page)

    @property
    def history(self):
        return self._history

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value


class SingleTabGeometry:
    def __init__(self) -> None:
        self.rounding_radius = 8
        self.title: Optional[str] = None

        # Coordinates inside a parent window
        self.left: Optional[int] = None
        self.right: Optional[int] = None
        self.top: Optional[int] = None
        self.bottom: Optional[int] = None

        # Coordinates inside the tab
        self.icon_left: Optional[int] = None
        self.icon_right: Optional[int] = None
        self.icon_top: Optional[int] = None
        self.icon_bottom: Optional[int] = None

        self.text_left: Optional[int] = None
        self.text_right: Optional[int] = None

        self.close_button_left: Optional[int] = None
        self.close_button_right: Optional[int] = None
        self.close_button_top: Optional[int] = None
        self.close_button_bottom: Optional[int] = None

    @property
    def height(self):
        return (
            self.bottom - self.top
            if self.bottom is not None and self.top is not None
            else 0
        )

    @property
    def width(self):
        return (
            self.right - self.left
            if self.right is not None and self.left is not None
            else 0
        )


class TabsGeometryCalculator:
    def __init__(self) -> None:
        self.min_width = 150
        self.max_width = 450
        self.vertical_margin = 8
        self.horizontal_margin = 8
        self.icon_size = 16
        self.close_button_size = 10
        self.gap_icon_text = 8
        self.gap_text_close_button = 6
        self.vertical_gap_between_tabs = 4
        self.horizontal_gap_between_tabs = 4
        self._geometry: Optional[List[SingleTabGeometry]] = None

    @property
    def geometry(self) -> Optional[List[SingleTabGeometry]]:
        return self._geometry

    @property
    def full_height(self) -> int:
        """Return height of all rows of tabs"""
        if self._geometry is None:
            return 0

        if len(self._geometry) == 0:
            return 0

        return self._geometry[-1].bottom - self._geometry[0].top

    @property
    def rows_count(self) -> int:
        """Return number of rows in the geometry"""
        if self._geometry is None:
            return 0

        return len(self._geometry)

    def _calc_width(self, parent_width: int, tabs_count: int, rows_count: int) -> int:
        if tabs_count == 0:
            return self.max_width

        cols_count = math.ceil(tabs_count / rows_count)
        if cols_count == 1:
            parent_width_minus_gap = parent_width
        else:
            parent_width_minus_gap = parent_width - (cols_count - 1) * self.horizontal_gap_between_tabs

        return int(math.floor(parent_width_minus_gap / cols_count))

    def calc(
        self, tabs: List[TabInfo], parent_width: int, text_height: int
    ) -> List[SingleTabGeometry]:
        tabs_count = len(tabs)
        rows_count = 1
        while (
            width := self._calc_width(parent_width, tabs_count, rows_count)
        ) < self.min_width:
            rows_count += 1

        cols_count = parent_width // width

        if width > self.max_width:
            width = self.max_width

        # Shared geometry
        height = 2 * self.vertical_margin + max(
            text_height, self.icon_size, self.close_button_size
        )
        if height % 2 == 0:
            height += 1
        center_vertical = height // 2

        icon_left = self.horizontal_margin
        icon_right = icon_left + self.icon_size
        icon_top = center_vertical - self.icon_size // 2
        icon_bottom = icon_top + self.icon_size

        close_button_right = width - self.horizontal_margin
        close_button_left = close_button_right - self.close_button_size
        close_button_top = center_vertical - self.close_button_size // 2
        close_button_bottom = close_button_top + self.close_button_size

        text_left = icon_right + self.gap_icon_text
        text_right = close_button_left - self.gap_text_close_button

        self._geometry = []
        current_row = -1
        current_top = -(height + self.vertical_gap_between_tabs)
        current_left = 0
        for n, info in enumerate(tabs):
            current_col = n % cols_count
            if current_col == 0:
                current_row += 1
                current_left = 0
                current_top += height + self.vertical_gap_between_tabs

            geometry = SingleTabGeometry()

            geometry.left = current_left
            geometry.right = geometry.left + width
            geometry.top = current_top
            geometry.bottom = geometry.top + height

            geometry.title = info.title
            geometry.icon_left = icon_left
            geometry.icon_right = icon_right
            geometry.icon_top = icon_top
            geometry.icon_bottom = icon_bottom

            geometry.text_left = text_left
            geometry.text_right = text_right

            geometry.close_button_left = close_button_left
            geometry.close_button_right = close_button_right
            geometry.close_button_top = close_button_top
            geometry.close_button_bottom = close_button_bottom

            self._geometry.append(geometry)
            current_left += width + self.horizontal_gap_between_tabs

        return self._geometry


class TabRender:
    def __init__(self, theme: Theme) -> None:
        self._theme = theme
        self._brushes = wx.BrushList()
        self._pens = wx.PenList()
        self._title_font = wx.NullFont

    def get_text_height(self, dc: wx.DC):
        text = "Wg"
        return dc.GetTextExtent(text).GetHeight()

    def _draw_icon(self, dc: wx.DC, tab: SingleTabGeometry) -> None:
        assert tab.icon_left is not None
        assert tab.icon_right is not None

        icon_rect = wx.Rect(
            tab.icon_left + tab.left,
            tab.icon_top + tab.top,
            tab.icon_right - tab.icon_left,
            tab.icon_bottom - tab.icon_top,
        )
        dc.DrawRectangle(icon_rect)

    def _draw_close_button(self, dc: wx.DC, tab: SingleTabGeometry) -> None:
        assert tab.close_button_left is not None
        assert tab.close_button_right is not None

        close_rect = wx.Rect(
            tab.close_button_left + tab.left,
            tab.close_button_top + tab.top,
            tab.close_button_right - tab.close_button_left,
            tab.close_button_bottom - tab.close_button_top,
        )
        dc.DrawRectangle(close_rect)

    def _trim_title(self, dc: wx.DC, title: str, max_width: int) -> str:
        def _get_trimmed_title(title: str, cut_count: int) -> str:
            if cut_count == 0:
                return title
            return title[:-cut_count] + "\u2026"

        cut_count = 0
        while (
            dc.GetTextExtent(_get_trimmed_title(title, cut_count)).GetWidth()
            > max_width
        ):
            cut_count += 1

        return _get_trimmed_title(title, cut_count)

    def _draw_title(self, dc: wx.DC, tab: SingleTabGeometry, state: int) -> None:
        assert tab.text_left is not None
        assert tab.text_right is not None
        assert tab.top is not None
        assert tab.left is not None
        assert tab.title is not None

        text_height = self.get_text_height(dc)
        text_top = tab.top + tab.height // 2 - text_height // 2
        text_max_width = tab.text_right - tab.text_left

        dc.SetFont(self._title_font)
        title = self._trim_title(dc, tab.title, text_max_width)
        dc.DrawText(title, tab.text_left + tab.left, text_top)

    def _draw_background(self, dc: wx.DC, tab: SingleTabGeometry) -> None:
        assert tab.left is not None
        assert tab.right is not None
        assert tab.top is not None
        assert tab.bottom is not None

        rect = wx.Rect(tab.left, tab.top, tab.right - tab.left, tab.bottom - tab.top)
        back_color = self._theme.colorBackground
        dc.SetPen(self._pens.FindOrCreatePen(back_color))
        dc.SetBrush(self._brushes.FindOrCreateBrush(back_color))
        dc.DrawRectangle(rect)

    def _draw_tab(self, dc: wx.DC, tab: SingleTabGeometry, state: int) -> None:
        assert tab.left is not None
        assert tab.right is not None
        assert tab.top is not None
        assert tab.bottom is not None

        # Get colors
        border_color = self._theme.get(Theme.SECTION_TABS, Theme.TABS_BORDER_COLOR)
        background_color = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_BACKGROUND_NORMAL_COLOR
        )
        if state == TAB_STATE_SELECTED:
            background_color = self._theme.get(
                Theme.SECTION_TABS, Theme.TABS_BACKGROUND_SELECTED_COLOR
            )
        elif state == TAB_STATE_HOVER:
            background_color = self._theme.get(
                Theme.SECTION_TABS, Theme.TABS_BACKGROUND_HOVER_COLOR
            )

        dc.SetPen(self._pens.FindOrCreatePen(border_color, 2))
        dc.SetBrush(
            self._brushes.FindOrCreateBrush(background_color, wx.BRUSHSTYLE_TRANSPARENT)
        )

        # Draw rounded tab
        r = tab.rounding_radius
        line_list = [
            (tab.left + r, tab.top, tab.right - r, tab.top),
            (tab.left, tab.top + r, tab.left, tab.bottom),
            (tab.right, tab.top + r, tab.right, tab.bottom),
            (tab.left, tab.bottom, tab.right, tab.bottom),
        ]
        dc.DrawLineList(line_list)
        dc.DrawArc(
            tab.left + r, tab.top, tab.left, tab.top + r, tab.left + r, tab.top + r
        )
        dc.DrawArc(
            tab.right, tab.top + r, tab.right - r, tab.top, tab.right - r, tab.top + r
        )

        dc.SetBrush(self._brushes.FindOrCreateBrush(background_color))
        dc.FloodFill(
            (tab.left + tab.right) // 2,
            (tab.bottom + tab.top) // 2,
            border_color,
            wx.FLOOD_BORDER,
        )

    def paint(self, dc: wx.DC, tab: SingleTabGeometry, state: int) -> None:
        font_size = self.get_default_font_size()
        self._title_font = wx.Font(wx.FontInfo(font_size))
        self._title_font.SetWeight(
            wx.FONTWEIGHT_BOLD if state == TAB_STATE_SELECTED else wx.FONTWEIGHT_NORMAL
        )

        self._draw_background(dc, tab)
        self._draw_tab(dc, tab, state)
        self._draw_icon(dc, tab)
        self._draw_title(dc, tab, state)
        self._draw_close_button(dc, tab)

    def get_default_font_size(self) -> int:
        return wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()

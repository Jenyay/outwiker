from dataclasses import dataclass
import logging
import math
import os.path
from typing import List, Optional, Tuple

from outwiker.core.tree import WikiPage
from outwiker.gui.theme import Theme
import wx
import wx.lib.newevent

from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.core.application import Application
from outwiker.core.history import History
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache
from outwiker.gui.images import readImage


TabsCtrlPageChangedEvent, EVT_TABSCTRL_PAGE_CHANGED = wx.lib.newevent.NewEvent()
TabsCtrlContextMenuEvent, EVT_TABSCTRL_CONTEXT_MENU = wx.lib.newevent.NewEvent()
TabsCtrlAddNewTabEvent, EVT_TABSCTRL_ADD_NEW_TAB = wx.lib.newevent.NewEvent()
TabsCtrlEndDragTabEvent, EVT_TABSCTRL_END_DRAG_TAB = wx.lib.newevent.NewEvent()
TabsCtrlPageClosedEvent, EVT_TABSCTRL_CLOSED_TAB = wx.lib.newevent.NewEvent()

TAB_STATE_NORMAL = 0
TAB_STATE_HOVER = 1
TAB_STATE_DOWNED = 2
TAB_STATE_DRAGGED = 3
TAB_STATE_SELECTED = 4
TAB_CLOSE_BUTTON_STATE_NORMAL = 0
TAB_CLOSE_BUTTON_STATE_HOVER = 1
TAB_CLOSE_BUTTON_STATE_DOWNED = 2
ADD_BUTTON_STATE_NORMAL = 0
ADD_BUTTON_STATE_HOVER = 1
ADD_BUTTON_STATE_DOWNED = 2


logger = logging.getLogger("outwiker.app.gui.tabsctrl2")


class TabsCtrl(wx.Window):
    def __init__(self, parent: wx.Window, application: Application, theme: Theme):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._application = application
        self._theme = theme

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # Min cursor moving to start drag tabs
        self._drag_delta = 5

        self._tabs: List[TabInfo] = []
        self._lbutton_downed_tab: Optional[int] = None
        self._lbutton_downed_close_button: Optional[int] = None
        self._rbutton_downed_tab: Optional[int] = None
        self._selected_tab: Optional[int] = None
        self._hovered_tab: Optional[int] = None
        self._hovered_close_button: Optional[int] = None
        self._dragged_tab: Optional[int] = None
        self._lbutton_down_coord: Optional[Tuple[int, int]] = None

        self._add_button_state = ADD_BUTTON_STATE_NORMAL

        self._current_rows_count = 0

        self._brushes = wx.BrushList()
        self._geometry = TabsGeometryCalculator(self._theme)
        self._tab_render = TabRender(self._theme)

        self.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW, handler=self._onMouseLeaveWindow)
        self.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftButtonDown)
        self.Bind(wx.EVT_RIGHT_UP, handler=self._onRightButtonUp)
        self.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightButtonDown)
        self.Bind(wx.EVT_LEFT_UP, handler=self._onLeftButtonUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleButtonDown)
        self.Bind(wx.EVT_SIZE, handler=self._onSize)
        self.Bind(wx.EVT_MOTION, handler=self._onMouseMove)

        self.Recalculate()

    def _clear_tabs_status(self) -> None:
        self._lbutton_downed_tab = None
        self._lbutton_downed_close_button = None
        self._rbutton_downed_tab = None
        self._dragged_tab = None
        self._lbutton_down_coord = None

        if self._add_button_state != ADD_BUTTON_STATE_NORMAL:
            self._add_button_state = ADD_BUTTON_STATE_NORMAL
            self._refresh_add_button()

        old_hovered_tab = self._hovered_tab
        if self._hovered_tab is not None or self._hovered_close_button is not None:
            self._hovered_tab = None
            self._hovered_close_button = None
            self._refresh_tab(old_hovered_tab)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)

    def Recalculate(self):
        self._calc_geometry()
        self.SetMinSize((-1, self._geometry.full_height))
        rows_count = self._geometry.rows_count

        if rows_count != self._current_rows_count:
            self._current_rows_count = rows_count
            self.GetParent().Layout()

        self.Refresh(False)

    def _calc_geometry(self):
        with wx.ClientDC(self) as dc:
            text_height = self._tab_render.get_text_height(dc)
        panel_width = self.GetClientSize()[0]
        panel_height = self.GetClientSize()[1]
        self._geometry.calc(self._tabs, panel_width, panel_height, text_height)

    def _onSize(self, event: wx.SizeEvent) -> None:
        self.Recalculate()

    def _onMouseLeaveWindow(self, event: wx.MouseEvent) -> None:
        self._clear_tabs_status()

    def _onLeftButtonDown(self, event: wx.MouseEvent) -> None:
        self._clear_tabs_status()

        if self._is_over_add_button(event.GetX(), event.GetY()):
            self._add_button_state = ADD_BUTTON_STATE_DOWNED
            return

        close_button_number = self._find_close_button_by_coord(
            event.GetX(), event.GetY()
        )
        self._lbutton_downed_close_button = close_button_number
        self._hovered_tab = self._find_tab_by_coord(event.GetX(), event.GetY())

        if close_button_number is None:
            self._lbutton_downed_tab = self._hovered_tab
            self._lbutton_down_coord = (event.GetX(), event.GetY())

    def _onLeftButtonUp(self, event: wx.MouseEvent) -> None:
        # Click on the "Add new tab" button
        if (
            self._add_button_state == ADD_BUTTON_STATE_DOWNED
            and self._is_over_add_button(event.GetX(), event.GetY())
        ):
            new_event = TabsCtrlAddNewTabEvent()
            wx.PostEvent(self, new_event)
            self._clear_tabs_status()
            return

        # Click on the close button
        close_button_number = self._find_close_button_by_coord(
            event.GetX(), event.GetY()
        )
        if (
            close_button_number is not None
            and close_button_number == self._lbutton_downed_close_button
        ):
            self._clear_tabs_status()
            self.ClosePage(close_button_number)
            return

        # Click on the tab
        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        if (
            tab_number is not None
            and tab_number == self._lbutton_downed_tab
            and tab_number != self._selected_tab
        ):
            self.SetSelection(tab_number)

        self._clear_tabs_status()
        self._hovered_tab = self._find_tab_by_coord(event.GetX(), event.GetY())
        self._hovered_close_button = self._find_close_button_by_coord(
            event.GetX(), event.GetY()
        )

    def _onRightButtonDown(self, event: wx.MouseEvent) -> None:
        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        self._rbutton_downed_tab = tab_number

    def _onRightButtonUp(self, event: wx.MouseEvent) -> None:
        old_tab_number = self._rbutton_downed_tab
        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())

        self._clear_tabs_status()
        if tab_number != old_tab_number:
            return

        page = self.GetPage(tab_number)
        if page is not None:
            new_event = TabsCtrlContextMenuEvent(page=page)
            wx.PostEvent(self, new_event)

    def _onMiddleButtonDown(self, event: wx.MouseEvent) -> None:
        self._clear_tabs_status()

        tab_number = self._find_tab_by_coord(event.GetX(), event.GetY())
        if tab_number is not None:
            self.ClosePage(tab_number)

    def _onMouseMove(self, event: wx.MouseEvent) -> None:
        old_hovered_tab = self._hovered_tab
        self._hovered_tab = self._find_tab_by_coord(event.GetX(), event.GetY())

        old_hovered_close_button = self._hovered_close_button
        self._hovered_close_button = self._find_close_button_by_coord(
            event.GetX(), event.GetY()
        )
        # Is drag tab?
        if event.LeftIsDown():
            # Start grag?
            if (
                self._dragged_tab is None
                and self._lbutton_downed_tab is not None
                and (
                    abs(event.GetX() - self._lbutton_down_coord[0]) >= self._drag_delta
                    or abs(event.GetY() - self._lbutton_down_coord[1])
                    >= self._drag_delta
                )
            ):
                self._dragged_tab = self._lbutton_downed_tab
                self._lbutton_downed_tab = None
                self.Recalculate()
                return

            if self._dragged_tab is not None:
                if self._hovered_tab is not None and self._dragged_tab != self._hovered_tab:
                    self.MovePage(self._dragged_tab, self._hovered_tab)
                    pass
                return

        # "Add new tab" button
        old_add_button_state = self._add_button_state
        is_add_button_hover = self._is_over_add_button(event.GetX(), event.GetY())
        if old_add_button_state == ADD_BUTTON_STATE_NORMAL and is_add_button_hover:
            self._add_button_state = ADD_BUTTON_STATE_HOVER
            self._refresh_add_button()
        elif (
            old_add_button_state != ADD_BUTTON_STATE_NORMAL and not is_add_button_hover
        ):
            self._add_button_state = ADD_BUTTON_STATE_NORMAL
            self._refresh_add_button()

        # "Close" button
        old_downed_close_button = self._lbutton_downed_close_button
        if self._hovered_close_button is None:
            self._lbutton_downed_close_button = None

        # Tab
        if old_hovered_tab != self._hovered_tab:
            if old_hovered_tab is not None:
                self._refresh_tab(old_hovered_tab)
            if self._hovered_tab is not None:
                self._refresh_tab(self._hovered_tab)

            if self._hovered_tab is not None:
                page = self._tabs[self._hovered_tab].page
                tooltip = f"{page.display_title}"
                self.SetToolTip(tooltip)
            else:
                self.UnsetToolTip()
        elif self._hovered_tab is not None and (
            old_hovered_close_button != self._hovered_close_button
            or old_downed_close_button != self._lbutton_downed_close_button
        ):
            self._refresh_tab(self._hovered_tab)

    def _find_tab_by_coord(self, x: int, y: int) -> Optional[int]:
        if self._geometry.geometry is None:
            return None

        for n, tab in enumerate(self._geometry.geometry):
            if x >= tab.left and x <= tab.right and y >= tab.top and y <= tab.bottom:
                return n

        return None

    def _find_close_button_by_coord(self, x: int, y: int) -> Optional[int]:
        if self._geometry.geometry is None:
            return None

        for n, tab in enumerate(self._geometry.geometry):
            button_left = tab.close_button.left
            button_right = tab.close_button.right
            button_top = tab.close_button.top
            button_bottom = tab.close_button.bottom

            if (
                x >= button_left
                and x <= button_right
                and y >= button_top
                and y <= button_bottom
            ):
                return n

        return None

    def _is_over_add_button(self, x: int, y: int) -> bool:
        if self._geometry.geometry is None:
            return False

        assert self._geometry.add_button is not None

        return (
            x >= self._geometry.add_button.left
            and x <= self._geometry.add_button.right
            and y >= self._geometry.add_button.top
            and y <= self._geometry.add_button.bottom
        )

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

    def HitTest(self, coord: Tuple[int, int]) -> Optional[WikiPage]:
        return self.GetPage(self._find_tab_by_coord(coord[0], coord[1]))

    def AddPage(self, page: Optional[WikiPage], title: str, select: bool = False):
        self._tabs.append(TabInfo(page, title))
        if len(self._tabs) == 1:
            self.SetSelection(0)
        elif select:
            self.SetSelection(len(self._tabs) - 1)

        self.Recalculate()

    def InsertPage(self, index: int, title: str, page: WikiPage, select: bool):
        self._tabs.insert(index, TabInfo(page, title))
        if select:
            self.SetSelection(index)

        self.Recalculate()
        self._updateHistoryButtons()

    def Clear(self):
        self.SetSelection(None)
        self._tabs.clear()
        self.Recalculate()
        self._updateHistoryButtons()

    def GetPageText(self, index):
        return self._tabs[index].title

    def RenameCurrentTab(self, title):
        page_index = self.GetSelection()
        if page_index is not None:
            self.RenameTab(page_index, title)

        self.Recalculate()

    def RenameTab(self, index, title):
        self._tabs[index].title = title
        self.Recalculate()

    def GetPage(self, index: Optional[int]) -> Optional[WikiPage]:
        return self._tabs[index].page if index is not None else None

    def SetCurrentPage(self, page: Optional[WikiPage], title: str):
        page_index = self.GetSelection()
        if page_index is not None:
            self._tabs[page_index].page = page
            self._tabs[page_index].title = title
            self._refresh_tab(page_index)
        elif page is not None:
            assert len(self._tabs) == 0
            self.AddPage(page, title)

        self._updateHistoryButtons()

    def _refresh_tab(self, page_index):
        assert self._geometry.geometry is not None
        if page_index is not None and page_index < len(self._tabs):
            self._calc_geometry()
            tab = self._geometry.geometry[page_index]
            self.Refresh(False, wx.Rect(tab.left, tab.top, tab.width, tab.height))

    def _refresh_add_button(self):
        assert self._geometry.add_button is not None
        self.Refresh(
            False,
            wx.Rect(
                self._geometry.add_button.left,
                self._geometry.add_button.top,
                self._geometry.add_button.width,
                self._geometry.add_button.height,
            ),
        )

    def _getCurrentHistory(self):
        """
        Возвращает класс истории для текущей вкладки
        """
        page_index = self.GetSelection()

        if page_index is not None:
            return self._tabs[page_index].history

    def GetSelection(self) -> Optional[int]:
        return self._selected_tab

    def GetPages(self):
        return [self.GetPage(index) for index in range(self.GetPageCount())]

    def GetPageCount(self):
        return len(self._tabs)

    def SetSelection(self, index: Optional[int]):
        old_selection = self._selected_tab
        self._selected_tab = index
        self._updateHistoryButtons()

        if old_selection is not None:
            self._refresh_tab(old_selection)

        if index is not None:
            self._refresh_tab(index)

        page = self._tabs[index].page if index is not None else None
        event = TabsCtrlPageChangedEvent(selection=index, page=page)
        wx.PostEvent(self, event)
        wx.SafeYield()

    def ClosePage(self, index: int):
        assert self._selected_tab is not None

        old_selection = self._selected_tab
        is_delete_selection = index == old_selection
        is_delete_before = index < old_selection
        page = self._tabs[index].page

        if index < len(self._tabs):
            del self._tabs[index]

        if is_delete_before:
            self._selected_tab -= 1
        elif is_delete_selection:
            new_count = len(self._tabs)
            new_index = old_selection
            if new_index >= new_count:
                new_index = new_count - 1

            if new_count == 0:
                new_index = None

            self.SetSelection(new_index)

        self.Recalculate()
        event = TabsCtrlPageClosedEvent(page=page)
        wx.PostEvent(self, event)

    def NextPage(self):
        count = len(self._tabs)
        old_selection = self._selected_tab
        if old_selection is None and count != 0:
            self.SetSelection(0)
            return

        if old_selection is not None and old_selection < count - 1:
            self.SetSelection(old_selection + 1)

        # After the last page switch to the first page
        if old_selection is not None and old_selection == count - 1 and count > 1:
            self.SetSelection(0)

    def PreviousPage(self):
        count = len(self._tabs)
        old_selection = self._selected_tab
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

    def MovePage(self, index: int, new_index: int):
        """Change tab position"""
        if index == new_index:
            return

        assert self._selected_tab is not None

        moved_tab = self._tabs[index]
        old_selected_tab = self._selected_tab
        move_selected = index == old_selected_tab

        del self._tabs[index]
        self._tabs.insert(new_index, moved_tab)
        if move_selected:
            self._selected_tab = new_index
        elif index < old_selected_tab and new_index >= old_selected_tab:
            self._selected_tab -= 1
        elif index > old_selected_tab and new_index <= old_selected_tab:
            self._selected_tab += 1

        self._dragged_tab = new_index
        self._hovered_tab = new_index

        self.Recalculate()

        event = TabsCtrlEndDragTabEvent()
        wx.PostEvent(self, event)

    def _onPaint(self, event: wx.PaintEvent):
        """
        Обработчик события перерисовки вкладок
        """
        with wx.BufferedPaintDC(self) as dc:
            background_brush = self._brushes.FindOrCreateBrush(
                self._theme.colorBackground
            )
            dc.SetBackground(background_brush)
            dc.Clear()

            if self._geometry.geometry is None:
                return

            for n, tab in enumerate(self._geometry.geometry):
                state = TAB_STATE_NORMAL
                if n == self._selected_tab:
                    state = TAB_STATE_SELECTED
                elif n == self._dragged_tab:
                    state = TAB_STATE_DRAGGED
                elif n == self._lbutton_downed_tab:
                    state = TAB_STATE_DOWNED
                elif n == self._hovered_tab:
                    state = TAB_STATE_HOVER

                close_button_state = TAB_CLOSE_BUTTON_STATE_NORMAL
                if n == self._hovered_close_button:
                    close_button_state = TAB_CLOSE_BUTTON_STATE_HOVER

                if n == self._lbutton_downed_close_button:
                    close_button_state = TAB_CLOSE_BUTTON_STATE_DOWNED

                self._tab_render.draw_tab(dc, tab, state, close_button_state)

            self._tab_render.draw_add_button(dc, self._geometry, self._add_button_state)


class TabInfo:
    def __init__(self, page, title: str):
        self._page = page
        self._title = title
        self._history = History()
        self._history.goto(page)

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page):
        self._page = page
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
        return self._page.icon if self._page is not None else None


class SingleTabGeometry:
    def __init__(self) -> None:
        self.rounding_radius = 8
        self.title: Optional[str] = None
        self.page_path: Optional[str] = None
        self.icon_file: Optional[str] = None

        # Coordinates inside a parent window
        self.left: Optional[int] = None
        self.right: Optional[int] = None
        self.top: Optional[int] = None
        self.bottom: Optional[int] = None

        self.icon: Optional[Rect] = None
        self.close_button: Optional[Rect] = None

        self.text_left: Optional[int] = None
        self.text_right: Optional[int] = None

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


@dataclass
class Rect:
    left: int
    right: int
    top: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top


class TabsGeometryCalculator:
    def __init__(self, theme: Theme) -> None:
        self._theme = theme
        self.min_width = 150
        self.max_width = 450
        self.vertical_margin = 5
        self.horizontal_margin = 8
        self.gap_icon_text = 8
        self.gap_text_close_button = 6
        self.vertical_gap_between_tabs = 4
        self.horizontal_gap_after_tab = 4

        self._geometry: Optional[List[SingleTabGeometry]] = None
        self.add_button: Optional[Rect] = None
        self.rows_count = 0

    @property
    def geometry(self) -> Optional[List[SingleTabGeometry]]:
        return self._geometry

    @property
    def full_height(self) -> int:
        """Return height of all rows of tabs"""
        if not self._geometry:
            return self._calc_tab_height(text_height=14)

        return self._geometry[-1].bottom - self._geometry[0].top

    def _calc_width(self, tabs_count: int, max_width: int) -> int:
        if max_width <= self.min_width:
            width = self.min_width
        else:
            rows_count = 1
            width = 0
            while width < self.min_width:
                cols_count = math.ceil(tabs_count / rows_count)
                if cols_count == 1:
                    parent_width_minus_gap = max_width
                else:
                    parent_width_minus_gap = (
                        max_width - (cols_count - 1) * self.horizontal_gap_after_tab
                    )

                width = int(math.floor(parent_width_minus_gap / cols_count))

                if width > self.max_width:
                    width = self.max_width
                rows_count += 1

        return width

    def _calc_rect(
        self,
        parent_width: int,
        parent_height: int,
        tabs_count: int,
        tab_height: int,
        add_button_size: int,
    ) -> Tuple[List[Rect], int]:
        if tabs_count == 0:
            return ([], 0)

        add_button_width = add_button_size
        max_width = parent_width - self.horizontal_gap_after_tab - add_button_width
        width = self._calc_width(tabs_count, max_width)

        # Calculate tabs border
        rect_list: List[Rect] = []
        current_left = 0
        current_top = 0
        rows_count = 1
        for n in range(tabs_count):
            if current_left + width > max_width:
                current_left = 0
                current_top += tab_height + self.vertical_gap_between_tabs
                rows_count += 1

            rect = Rect(
                current_left,
                current_left + width,
                current_top,
                current_top + tab_height,
            )
            rect_list.append(rect)
            current_left += width + self.horizontal_gap_after_tab

        # Move tabs to bottom of parent window
        if rect_list and rect_list[-1].bottom - rect_list[0].top < parent_height:
            delta = parent_height - (rect_list[-1].bottom - rect_list[0].top)
            for rect in rect_list:
                rect.top += delta
                rect.bottom += delta

        return (rect_list, rows_count)

    def _calc_tab_height(self, text_height: int) -> int:
        icon_size = self._theme.get(Theme.SECTION_TABS, Theme.TABS_ICON_SIZE)
        close_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_CLOSE_BUTTON_SIZE
        )
        add_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE
        )

        height = 2 * self.vertical_margin + max(
            text_height, icon_size, close_button_size, add_button_size
        )

        if height % 2 == 0:
            height += 1

        return height

    def calc(
        self,
        tabs: List[TabInfo],
        parent_width: int,
        parent_height: int,
        text_height: int,
    ) -> List[SingleTabGeometry]:
        icon_size = self._theme.get(Theme.SECTION_TABS, Theme.TABS_ICON_SIZE)
        close_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_CLOSE_BUTTON_SIZE
        )
        add_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE
        )

        height = self._calc_tab_height(text_height)

        center_vertical = height // 2
        rect_list, self.rows_count = self._calc_rect(
            parent_width, parent_height, len(tabs), height, add_button_size
        )

        self._geometry = []
        for info, rect in zip(tabs, rect_list):
            geometry = SingleTabGeometry()

            geometry.left = rect.left
            geometry.right = rect.right
            geometry.top = rect.top
            geometry.bottom = rect.bottom

            geometry.title = info.title
            geometry.page_path = info.page.path if info.page is not None else None
            geometry.icon_file = info.page.icon if info.page is not None else None

            icon_left = self.horizontal_margin + geometry.left
            icon_right = icon_left + icon_size
            icon_top = center_vertical - icon_size // 2 + geometry.top
            icon_bottom = icon_top + icon_size
            geometry.icon = Rect(icon_left, icon_right, icon_top, icon_bottom)

            close_button_right = rect.width - self.horizontal_margin + geometry.left
            close_button_left = close_button_right - close_button_size
            close_button_top = center_vertical - close_button_size // 2 + geometry.top
            close_button_bottom = close_button_top + close_button_size
            geometry.close_button = Rect(
                close_button_left,
                close_button_right,
                close_button_top,
                close_button_bottom,
            )

            geometry.text_left = geometry.icon.right + self.gap_icon_text
            geometry.text_right = (
                geometry.close_button.left - self.gap_text_close_button
            )

            self._geometry.append(geometry)

        # Calculate "Add new tab" button position
        if self._geometry:
            add_button_left = self._geometry[-1].right + self.horizontal_gap_after_tab
            add_button_top = (
                self._geometry[-1].top + center_vertical - add_button_size // 2
            )
        else:
            add_button_left = self.horizontal_gap_after_tab
            add_button_top = parent_height // 2 - add_button_size // 2

        add_button_right = add_button_left + add_button_size
        add_button_bottom = add_button_top + add_button_size
        self.add_button = Rect(
            add_button_left, add_button_right, add_button_top, add_button_bottom
        )
        return self._geometry


class TabRender:
    def __init__(self, theme: Theme) -> None:
        self._theme = theme
        self._brushes = wx.BrushList()
        self._pens = wx.PenList()
        self._title_font = wx.NullFont

        # "Close" button
        close_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_CLOSE_BUTTON_SIZE
        )
        self._close_button_normal_bmp = readImage(
            getBuiltinImagePath("close_tab_normal.svg"),
            close_button_size,
            close_button_size,
        )
        self._close_button_hover_bmp = readImage(
            getBuiltinImagePath("close_tab_hover.svg"),
            close_button_size,
            close_button_size,
        )
        self._close_button_downed_bmp = readImage(
            getBuiltinImagePath("close_tab_downed.svg"),
            close_button_size,
            close_button_size,
        )

        # "Add new tab" button
        add_button_size = self._theme.get(
            Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE
        )
        self._add_button_normal_bmp = readImage(
            getBuiltinImagePath("add_tab_normal.svg"),
            add_button_size,
            add_button_size,
        )
        self._add_button_hover_bmp = readImage(
            getBuiltinImagePath("add_tab_hover.svg"),
            add_button_size,
            add_button_size,
        )
        self._add_button_downed_bmp = readImage(
            getBuiltinImagePath("add_tab_downed.svg"),
            add_button_size,
            add_button_size,
        )

        # Main icons for notes
        self._defaultIcon = getBuiltinImagePath("page.svg")
        icon_size = self._theme.get(Theme.SECTION_TABS, Theme.TABS_ICON_SIZE)
        self._iconsCache = ImageListCache(self._defaultIcon, icon_size, icon_size)

    def _load_icon(
        self, icon_file: Optional[str], page_path: Optional[str]
    ) -> Optional[int]:
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        if page_path is None:
            return None

        if not icon_file:
            return self._iconsCache.getDefaultImageId()

        icon_file = os.path.abspath(icon_file)
        page_path = os.path.abspath(page_path)

        try:
            if icon_file.startswith(page_path):
                imageId = self._iconsCache.replace(icon_file)
            else:
                imageId = self._iconsCache.add(icon_file)
        except Exception:
            logger.error("Invalid icon file: %s", icon_file)
            imageId = self._iconsCache.getDefaultImageId()
        return imageId

    def get_text_height(self, dc: wx.DC):
        text = "Wg"
        return dc.GetTextExtent(text).GetHeight()

    def _draw_icon(self, dc: wx.DC, tab: SingleTabGeometry) -> None:
        assert tab.icon is not None

        icon_id = self._load_icon(tab.icon_file, tab.page_path)
        if icon_id is not None:
            bitmap = self._iconsCache.getImageList().GetBitmap(icon_id)
            assert bitmap.IsOk()
            dc.DrawBitmap(bitmap, tab.icon.left, tab.icon.top)

    def _draw_close_button(
        self, dc: wx.DC, tab: SingleTabGeometry, close_button_state: int
    ) -> None:
        assert tab.close_button is not None

        if close_button_state == TAB_CLOSE_BUTTON_STATE_HOVER:
            dc.DrawBitmap(
                self._close_button_hover_bmp,
                tab.close_button.left,
                tab.close_button.top,
            )
        elif close_button_state == TAB_CLOSE_BUTTON_STATE_DOWNED:
            dc.DrawBitmap(
                self._close_button_downed_bmp,
                tab.close_button.left,
                tab.close_button.top,
            )
        else:
            dc.DrawBitmap(
                self._close_button_normal_bmp,
                tab.close_button.left,
                tab.close_button.top,
            )

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
        assert tab.title is not None

        text_height = self.get_text_height(dc)
        text_top = tab.height // 2 - text_height // 2 + tab.top
        text_max_width = tab.text_right - tab.text_left

        dc.SetFont(self._title_font)
        title = self._trim_title(dc, tab.title, text_max_width)
        dc.DrawText(title, tab.text_left, text_top)

    def _draw_background(self, dc: wx.DC, tab: SingleTabGeometry) -> None:
        assert tab.left is not None
        assert tab.right is not None
        assert tab.top is not None
        assert tab.bottom is not None

        rect = wx.Rect(tab.left, tab.top, tab.width, tab.height)
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
        elif state == TAB_STATE_DRAGGED:
            background_color = self._theme.get(
                Theme.SECTION_TABS, Theme.TABS_BACKGROUND_DRAGGED_COLOR
            )
        elif state == TAB_STATE_DOWNED:
            background_color = self._theme.get(
                Theme.SECTION_TABS, Theme.TABS_BACKGROUND_DOWNED_COLOR
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

    def draw_tab(
        self, dc: wx.DC, tab: SingleTabGeometry, tab_state: int, close_button_state: int
    ) -> None:
        font_size = self.get_default_font_size()
        self._title_font = wx.Font(wx.FontInfo(font_size))
        self._title_font.SetWeight(
            wx.FONTWEIGHT_BOLD
            if tab_state == TAB_STATE_SELECTED
            else wx.FONTWEIGHT_NORMAL
        )

        self._draw_background(dc, tab)
        self._draw_tab(dc, tab, tab_state)
        self._draw_icon(dc, tab)
        self._draw_title(dc, tab, tab_state)
        self._draw_close_button(dc, tab, close_button_state)

    def draw_add_button(
        self, dc: wx.DC, geometry: TabsGeometryCalculator, add_button_state: int
    ) -> None:
        if add_button_state == ADD_BUTTON_STATE_HOVER:
            dc.DrawBitmap(
                self._add_button_hover_bmp,
                geometry.add_button.left,
                geometry.add_button.top,
            )
        elif add_button_state == ADD_BUTTON_STATE_DOWNED:
            dc.DrawBitmap(
                self._add_button_downed_bmp,
                geometry.add_button.left,
                geometry.add_button.top,
            )
        else:
            dc.DrawBitmap(
                self._add_button_normal_bmp,
                geometry.add_button.left,
                geometry.add_button.top,
            )

    def get_default_font_size(self) -> int:
        return wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize()

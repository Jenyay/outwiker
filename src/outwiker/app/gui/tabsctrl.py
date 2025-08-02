import math
from typing import List, Optional

from outwiker.gui.theme import Theme
import wx
import wx.lib.newevent

from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.core.application import Application
from outwiker.core.history import History


TabsCtrlPageChangedEvent, EVT_TABSCTRL_PAGE_CHANGED = wx.lib.newevent.NewEvent()


class TabsCtrl(wx.Control):
    def __init__(self, parent: wx.Window, application: Application, theme: Theme):
        super().__init__(parent)
        self._application = application
        self._theme = theme

        self._tabs_collection: List[TabInfo] = []
        self._current_page_index: Optional[int] = None

        # self._tabs = fnb.FlatNotebook(self,
        #                               agwStyle=(
        #                                   fnb.FNB_FF2 |
        #                                   fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS |
        #                                   fnb.FNB_X_ON_TAB |
        #                                   fnb.FNB_DROPDOWN_TABS_LIST))
        # self._tabs.SetPadding(wx.Size(10, -1))
        self.__layout()

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        # self._tabs.SetBackgroundColour(colour)
        # self._tabs.SetTabAreaColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        # self._tabs.SetForegroundColour(colour)

    def __layout(self):
        self.SetMinSize((-1, 48))
        # mainSizer = wx.FlexGridSizer(1, 0, 0, 0)

        # mainSizer.AddGrowableCol(0)
        # mainSizer.AddGrowableRow(0)

        # # mainSizer.Add(self._tabs, 0, wx.EXPAND)
        # self.SetSizer(mainSizer)
        # self.Layout()

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
        # blankWindow = TabInfo(page)
        # self._tabs.AddPage(blankWindow, title)

    def InsertPage(self, index, title, page, select):
        self._tabs_collection.insert(index, TabInfo(page, title))
        if select:
            self.SetSelection(index)
        # self._updateHistoryButtons()

    def Clear(self):
        # self._tabs.DeleteAllPages()
        self.SetSelection(None)
        self._tabs_collection.clear()
        # self._updateHistoryButtons()

    def GetPageText(self, index):
        # TODO: Cut off long page titles
        return self._tabs_collection[index].title
        # return self._tabs.GetPageText(index)

    def RenameCurrentTab(self, title):
        page_index = self.GetSelection()
        if page_index is not None:
            self.RenameTab(page_index, title)

    def RenameTab(self, index, title):
        self._tabs_collection[index].title = title
        # self._tabs.SetPageText(index, title)
        pass

    def GetPage(self, index: Optional[int]):
        # return self._tabs.GetPage(index).page
        return self._tabs_collection[index].page if index is not None else None

    def SetCurrentPage(self, page, title):
        page_index = self.GetSelection()
        if page_index is not None:
            self._tabs_collection[page_index].page = page
            self._tabs_collection[page_index].title = title
            # self._tabs.GetPage(page_index).page = page

        self._updateHistoryButtons()

    def _getCurrentHistory(self):
        """
        Возвращает класс истории для текущей вкладки
        """
        page_index = self.GetSelection()

        if page_index is not None:
            return self._tabs_collection[page_index].history
            # return self._tabs.GetPage(page_index).history

    def GetSelection(self) -> Optional[int]:
        # return self._tabs.GetSelection()
        return self._current_page_index

    def GetPages(self):
        return [self.GetPage(index) for index in range(self.GetPageCount())]

    def GetPageCount(self):
        return len(self._tabs_collection)

    def SetSelection(self, index: Optional[int]):
        # old_selected_page = self.GetPage(self._current_page_index)
        # new_selected_page = self.GetPage(index)
        # if old_selected_page is new_selected_page:
        #     return

        self._current_page_index = index
        self._updateHistoryButtons()
        page = self._tabs_collection[index].page if index is not None else None
        event = TabsCtrlPageChangedEvent(selection=index, page=page)
        wx.PostEvent(self, event)
        wx.SafeYield()

    def DeletePage(self, index):
        assert self._current_page_index is not None
        # self._tabs.DeletePage(index)
        old_selection = self._current_page_index
        is_delete_selection = index == old_selection
        is_delete_before = index < old_selection

        if index < len(self._tabs_collection):
            del self._tabs_collection[index]

        if is_delete_before:
            self._current_page_index -= 1
            return

        if is_delete_selection:
            new_count = len(self._tabs_collection)
            new_index = old_selection
            if new_index >= new_count:
                new_index = new_count - 1

            if new_count == 0:
                new_index = None

            self.SetSelection(new_index)
            # self._updateHistoryButtons()

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

        # self._tabs.AdvanceSelection(True)
        # self._updateHistoryButtons()

    def PreviousPage(self):
        # self._tabs.AdvanceSelection(False)
        # self._updateHistoryButtons()
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


class TabsGeometryCalculator:
    def __init__(self) -> None:
        self.min_width = 50
        self.max_width = 250
        self.vertical_margin = 4
        self.horizontal_margin = 4
        self.icon_size = 16
        self.close_button_size = 10
        self.gap_icon_text = 4
        self.gap_text_close_button = 4
        self.vertical_gap_between_tabs = 2
        self.horizontal_gap_between_tabs = 2
        self._geometry: Optional[List[List[SingleTabGeometry]]] = None

    @property
    def geometry(self) -> Optional[List[List[SingleTabGeometry]]]:
        return self._geometry

    def _calc_width(self, parent_width: int, tabs_count: int, rows_count: int) -> int:
        if tabs_count == 0:
            return self.max_width

        return int(math.floor(parent_width / (math.ceil(tabs_count / rows_count))))

    def calc(
        self, tabs: List[TabInfo], parent_width: int, text_height: int
    ) -> List[List[SingleTabGeometry]]:
        tabs_count = len(tabs)
        rows_count = 1
        while (
            width := self._calc_width(parent_width, tabs_count, rows_count)
        ) < self.min_width + self.horizontal_gap_between_tabs:
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
                self._geometry.append([])
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

            self._geometry[-1].append(geometry)
            current_left += width + self.horizontal_gap_between_tabs

        return self._geometry

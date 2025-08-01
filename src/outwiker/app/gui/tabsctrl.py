# -*- coding: utf-8 -*-
from typing import List, Optional

import wx
import wx.lib.newevent

from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.core.application import Application
from outwiker.core.history import History


TabsCtrlPageChangedEvent, EVT_TABSCTRL_PAGE_CHANGED = wx.lib.newevent.NewEvent()


class TabsCtrl(wx.Panel):
    def __init__(self, parent, application: Application):
        super().__init__(parent)
        self._application = application

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
                HistoryBackAction.stringId,
                False)
            self._application.actionController.enableTools(
                HistoryForwardAction.stringId,
                False)
        else:
            self._application.actionController.enableTools(
                HistoryBackAction.stringId,
                history.backLength != 0)
            self._application.actionController.enableTools(
                HistoryForwardAction.stringId,
                history.forwardLength != 0)

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

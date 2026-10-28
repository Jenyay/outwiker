# -*- coding: utf-8 -*-

from typing import List

import wx
import wx.lib.newevent
import wx.lib.agw.ultimatelistctrl as ULC

from outwiker.core.tree import WikiPage
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache
from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT
from .pagelist_columns import BaseColumn

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageList(wx.Panel):
    def __init__(self, parent: wx.Window, sortable: bool = True, selectable: bool = False):
        super().__init__(parent)
        self._columns: list[BaseColumn] = []
        self._pages: list[WikiPage] = []
        self._defaultIcon = getBuiltinImagePath("page.svg")
        self._imageList = ImageListCache(self._defaultIcon, ICONS_WIDTH, ICONS_HEIGHT)

        self._propagationLevel = 15
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self._sizer = wx.FlexGridSizer(cols=1)
        self._sizer.AddGrowableCol(0)
        self._sizer.AddGrowableRow(0)

        list_style = (
                ULC.ULC_REPORT
                | ULC.ULC_SINGLE_SEL
                | ULC.ULC_VRULES
                | ULC.ULC_HRULES
                | ULC.ULC_SHOW_TOOLTIPS
                )
        if not selectable:
            list_style |= ULC.ULC_NO_HIGHLIGHT

        self._listCtrl = ULC.UltimateListCtrl(self, agwStyle=list_style)

        self._listCtrl.Bind(ULC.EVT_LIST_ITEM_HYPERLINK, handler=self._onPageClick)

        if sortable:
            self._listCtrl.Bind(ULC.EVT_LIST_COL_CLICK, handler=self._onColClick)

        self._listCtrl.SetHyperTextNewColour(wx.BLUE)
        self._listCtrl.SetHyperTextVisitedColour(wx.BLUE)
        self._listCtrl.AssignImageList(
            self._imageList.getImageList(), wx.IMAGE_LIST_SMALL
        )

        self._sizer.Add(self._listCtrl, flag=wx.EXPAND)
        self.SetSizer(self._sizer)

    @property
    def listCtrl(self):
        return self._listCtrl

    @property
    def imageList(self):
        return self._imageList

    @property
    def _visibleColumns(self):
        return [col for col in self._columns if col.visible]

    def _onPageClick(self, event):
        item = event.GetItem()
        page = item.GetData()
        if page:
            assert page is not None
            event = PageClickEvent(page=page)
            event.ResumePropagation(self._propagationLevel)
            wx.PostEvent(self, event)

    def _onColClick(self, event):
        self.sortByColumn(event.GetColumn())

    def sortByColumn(self, col_index: int):
        for n, column in enumerate(self._visibleColumns):
            if n != col_index:
                column.set_sort_type(BaseColumn.SORT_NONE, self._listCtrl)

        column = self._visibleColumns[col_index]
        if column.sort_type == BaseColumn.SORT_NORMAL:
            column.set_sort_type(BaseColumn.SORT_INVERSE, self._listCtrl)
        else:
            column.set_sort_type(BaseColumn.SORT_NORMAL, self._listCtrl)

        if column.sort_type == BaseColumn.SORT_INVERSE:
            self._listCtrl.SortItems(column.sortFunctionInverse)
        else:
            self._listCtrl.SortItems(column.sortFunction)

    def clear(self):
        """
        Удалить все элементы из списка
        """
        self._listCtrl.ClearAll()

    def _createColumns(self):
        for n, column in enumerate(self._visibleColumns):
            column.insertColumn(self._listCtrl, n)

    def setPageList(self, pages: list[WikiPage]):
        """
        pages - список страниц, отображаемый в списке
        """
        self._pages = list(pages)
        self._updatePageList()

    def setColumns(self, columns: List[BaseColumn]):
        self._columns = columns
        self._updatePageList()

    def _updatePageList(self):
        self._listCtrl.Freeze()
        self.clear()
        self._createColumns()
        self._fillPageList()
        self._listCtrl.Thaw()

    def _fillPageList(self):
        for page in self._pages:
            self._insertPage(self._listCtrl.GetItemCount(), page)

    def _insertPage(self, position: int, page: WikiPage) -> int:
        """
        Insert the page into the specified position of the list.
        Return the index of the added item.
        """
        items = [column.getCellContent(page) for column in self._visibleColumns]
        self._listCtrl.InsertStringItem(position, items[0] if items else "")

        for n, column in enumerate(self._visibleColumns):
            if n > 0:
                self._listCtrl.SetStringItem(position, n, items[n])

            column.setCellProperties(self, position, n, page)

        self._listCtrl.SetItemData(position, page)
        return position

    def _findPageIndex(self, page: WikiPage) -> None | int:
        """
        Return the index of the page in the internal list or None if the page
        is not found.
        """
        for index, item_page in enumerate(self._pages):
            if item_page is page:
                return index

        return None

    def setItemPosition(self, src_position: int, new_position: int):
        """
        Move the item from src_position to new_position.
        """
        items_count = self._listCtrl.GetItemCount()
        if src_position < 0 or src_position >= items_count:
            return

        if new_position < 0 or new_position >= items_count:
            return

        if len(self._pages) != items_count:
            return

        if src_position == new_position:
            return

        selected_pages = [
            self._pages[index]
            for index in range(items_count)
            if self._listCtrl.IsSelected(index)
            ]

        page = self._pages.pop(src_position)
        self._pages.insert(new_position, page)

        self._updatePageList()

        first_selected = None
        for selected_page in selected_pages:
            index = self._findPageIndex(selected_page)
            if index is not None:
                self._listCtrl.Select(index)
                if first_selected is None:
                    first_selected = index

        if first_selected is not None:
            self._listCtrl.EnsureVisible(first_selected)

    def moveSelectedItemUp(self):
        """
        Move the first selected item one position up.
        """
        selected = self.getSelectedIndex()
        if selected is None:
            return

        self.setItemPosition(selected, selected - 1)

    def moveSelectedItemDown(self):
        """
        Move the first selected item one position down.
        """
        selected = self.getSelectedIndex()
        if selected is None:
            return

        self.setItemPosition(selected, selected + 1)

    def removeItem(self, index: int):
        """
        Remove the item with the specified index from the list.
        Do nothing if the index is out of range.
        """
        items_count = self._listCtrl.GetItemCount()
        if index < 0 or index >= items_count:
            return

        if len(self._pages) != items_count:
            self._listCtrl.DeleteItem(index)
            return

        self._pages.pop(index)
        self._updatePageList()

    def updateColumnsWidth(self):
        n = 0
        for col in self._columns:
            if not col.visible:
                continue

            col.width = self._listCtrl.GetColumnWidth(n)
            n += 1

    def getColumns(self) -> List[BaseColumn]:
        return self._columns

    def getSelectedIndex(self) -> None | int:
        for n in range(self.listCtrl.GetItemCount()):
            if self.listCtrl.IsSelected(n):
                return n
        return None

    def setSelected(self, index: int):
        for n in range(self.listCtrl.GetItemCount()):
            self.listCtrl.Select(n, n == index)

# -*- coding: utf-8 -*-

import os
from typing import List

import wx
import wx.lib.newevent

import outwiker.gui.controls.ultimatelistctrl as ULC
from outwiker.core.system import getImagesDir
from outwiker.gui.imagelistcache import ImageListCache
from .pagelist_columns import BaseColumn

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageData(object):
    def __init__(self, page):
        self.page = page


class PageList(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self._columns = []                     # type: List[BaseColumn]
        self._pages = []
        self._defaultIcon = os.path.join(getImagesDir(), "page.png")
        self._imageList = ImageListCache(self._defaultIcon)

        # Key - MenuItem ID, value - item from self._columns
        self._popupMenuColumnItems = {}        # type: Dict[int, BaseColumn]

        self._propagationLevel = 15
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self._sizer = wx.FlexGridSizer(cols=1)
        self._sizer.AddGrowableCol(0)
        self._sizer.AddGrowableRow(0)

        self._listCtrl = ULC.UltimateListCtrl(
            self,
            agwStyle=ULC.ULC_REPORT | ULC.ULC_SINGLE_SEL | ULC.ULC_VRULES | ULC.ULC_HRULES | ULC.ULC_SHOW_TOOLTIPS | ULC.ULC_NO_HIGHLIGHT
        )

        self._listCtrl.Bind(ULC.EVT_LIST_ITEM_HYPERLINK,
                            handler=self._onPageClick)
        self._listCtrl.Bind(ULC.EVT_LIST_COL_CLICK,
                            handler=self._onColClick)
        self._listCtrl.Bind(ULC.EVT_LIST_COL_RIGHT_CLICK,
                            handler=self._onColRightClick)
        self._listCtrl.SetHyperTextNewColour(wx.BLUE)
        self._listCtrl.SetHyperTextVisitedColour(wx.BLUE)
        self._listCtrl.AssignImageList(self._imageList.getImageList(),
                                       wx.IMAGE_LIST_SMALL)

        self._sizer.Add(self._listCtrl, flag=wx.EXPAND)

        self.SetSizer(self._sizer)
        self.Bind(wx.EVT_MENU, handler=self._onPopupMenuClick)

    def _onPopupMenuClick(self, event):
        col = self._popupMenuColumnItems[event.GetId()]
        col.visible = not col.visible
        self._popupMenuColumnItems = {}
        self._updatePageList()

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
        pageData = item.GetPyData()
        if pageData:
            page = pageData.page
            assert page is not None
            event = PageClickEvent(page=page)
            event.ResumePropagation(self._propagationLevel)
            wx.PostEvent(self, event)

    def _onColClick(self, event):
        self.sortByColumn(event.GetColumn())

    def _onColRightClick(self, event):
        menu = wx.Menu()
        self._popupMenuColumnItems = {}

        for col in self._columns[1:]:
            menu_item = menu.AppendCheckItem(wx.ID_ANY, col.getTitle())
            menu_item.Check(col.visible)
            self._popupMenuColumnItems[menu_item.GetId()] = col

        self.PopupMenu(menu)

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

    def setPageList(self, pages):
        """
        pages - список страниц, отображаемый в списке
        """
        self._pages = pages
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
            items = [column.getCellContent(page)
                     for column
                     in self._visibleColumns]
            item_index = self._listCtrl.Append(items)
            for n, column in enumerate(self._visibleColumns):
                column.setCellProperties(self, item_index, n, page)

            data = PageData(page)
            self._listCtrl.SetItemPyData(item_index, data)

    def updateColumnsWidth(self):
        n = 0
        for col in self._columns:
            if not col.visible:
                continue

            col.width = self._listCtrl.GetColumnWidth(n)
            n += 1

    def getColumns(self) -> List[BaseColumn]:
        return self._columns

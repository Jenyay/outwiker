# -*- coding: utf-8 -*-

from typing import List

import wx
import wx.lib.newevent

import outwiker.gui.controls.ultimatelistctrl as ULC

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageData(object):
    def __init__(self, page):
        self.page = page


class BaseColumn(object):
    '''
    Base class to manage columns
    '''
    def __init__(self, title: str, width: int, visible=True):
        self.title = title
        self.width = width
        self.visible = visible

    def insertColumn(self, listCtrl: 'PageList', position: int):
        '''
        Add column
        '''
        listCtrl.InsertColumn(position, self.title)
        listCtrl.SetColumnWidth(position, self.width)

    def setCellProperties(self,
                          listCtrl: 'PageList',
                          item_index: ULC.UltimateListItem,
                          position: int):
        pass

    def getCellContent(self, page):
        pass


class PageTitleColumn(BaseColumn):
    '''
    Column with page title (link to page)
    '''
    def setCellProperties(self,
                          listCtrl: 'PageList',
                          item_index: ULC.UltimateListItem,
                          position: int):
        listCtrl.SetItemHyperText(item_index, position)

    def getCellContent(self, page):
        return page.display_title


class ParentPageColumn(BaseColumn):
    '''
    Column with page parent path
    '''
    def getCellContent(self, page):
        parent_page = page.parent
        if parent_page.parent:
            return parent_page.display_subpath + '/'

        return ''


class TagsColumn(BaseColumn):
    '''
    Column with page tags
    '''
    def getCellContent(self, page):
        return ', '.join(page.tags)


class ModifyDateColumn(BaseColumn):
    '''
    Column with modify date of page
    '''
    def getCellContent(self, page):
        return page.datetime.strftime('%d.%m.%Y     %H:%M')


class PageList(wx.Panel):
    def __init__(self, parent: wx.Window, columns: List[BaseColumn]):
        super().__init__(parent)
        self._columns = columns

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
        self._listCtrl.SetHyperTextNewColour(wx.BLUE)
        self._listCtrl.SetHyperTextVisitedColour(wx.BLUE)

        self._sizer.Add(self._listCtrl, flag=wx.EXPAND)

        self.SetSizer(self._sizer)

    def _onPageClick(self, event):
        item = event.GetItem()
        pageData = item.GetPyData()
        if pageData:
            page = pageData.page
            assert page is not None
            event = PageClickEvent(page=page)
            event.ResumePropagation(self._propagationLevel)
            wx.PostEvent(self, event)

    def clear(self):
        """
        Удалить все элементы из списка
        """
        self._listCtrl.ClearAll()

    @property
    def _visibleColumns(self):
        return [column for column in self._columns if column.visible]

    def _createColumns(self):
        for n, column in enumerate(self._visibleColumns):
            column.insertColumn(self._listCtrl, n)

    def setPageList(self, pages):
        """
        pages - список страниц, отображаемый в списке
        """
        self._listCtrl.Freeze()
        self.clear()
        self._createColumns()

        for page in pages:
            items = [column.getCellContent(page)
                     for column
                     in self._visibleColumns]
            item_index = self._listCtrl.Append(items)
            for n, column in enumerate(self._visibleColumns):
                column.setCellProperties(self._listCtrl, item_index, n)

            data = PageData(page)
            self._listCtrl.SetItemPyData(item_index, data)

        self._listCtrl.Thaw()

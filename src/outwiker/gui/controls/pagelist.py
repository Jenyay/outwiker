# -*- coding: utf-8 -*-

import os
from typing import List

import wx
import wx.lib.newevent

import outwiker.gui.controls.ultimatelistctrl as ULC
from outwiker.core.system import getImagesDir
from outwiker.gui.imagelistcache import ImageListCache

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()

WIDTH_DEFAULT = 200


class ColumnsFactory(object):
    def __init__(self):
        self._allColTypes = [PageTitleColumn,
                             ParentPageColumn,
                             TagsColumn,
                             ModifyDateColumn,
                             ]

    @property
    def typesCount(self):
        return len(self._allColTypes)

    def createColumn(self,
                     name: str,
                     width: int = WIDTH_DEFAULT,
                     visible: bool = True) -> 'BaseColumn':
        for col_type in self._allColTypes:
            if name == col_type.name:
                return col_type(width, visible)

        raise ValueError

    def createDefaultColumns(self) -> List['BaseColumn']:
        columns = []
        columns.append(PageTitleColumn(WIDTH_DEFAULT, True))
        columns.append(ParentPageColumn(WIDTH_DEFAULT, True))
        columns.append(TagsColumn(WIDTH_DEFAULT, True))
        columns.append(ModifyDateColumn(WIDTH_DEFAULT, True))

        assert len(columns) == self.typesCount
        return columns

    def createColumnsFromString(self, string: str) -> List['BaseColumn']:
        '''
        The function can raise ValueError exception.
        '''
        columns = []

        if not string.strip():
            return columns

        if ',' in string:
            item_params = [item_str.strip()
                           for item_str
                           in string.strip().split(',')]
        else:
            item_params = [string.strip()]

        for item in item_params:
            name, width, visible = item.split(':')
            width = int(width)
            visible = visible.lower() == 'true'
            column = self.createColumn(name, width, visible)
            columns.append(column)

        return columns

    def toString(self, columns: List['BaseColumn']) -> str:
        return ','.join(['{name}:{width}:{visible}'.format(name=col.name,
                                                           width=col.width,
                                                           visible=col.visible)
                         for col in columns])


class PageData(object):
    def __init__(self, page):
        self.page = page


class BaseColumn(object):
    '''
    Base class to manage columns
    '''
    def __init__(self, width: int, visible=True):
        self.width = width
        self.visible = visible

    def insertColumn(self, listCtrl: 'PageList', position: int):
        '''
        Add column
        '''
        listCtrl.InsertColumn(position, self.getTitle())
        listCtrl.SetColumnWidth(position, self.width)

    def setCellProperties(self,
                          pageList: 'PageList',
                          item_index: ULC.UltimateListItem,
                          position: int,
                          page):
        pass

    def getCellContent(self, page) -> str:
        pass

    def getTitle(self) -> str:
        pass


class PageTitleColumn(BaseColumn):
    '''
    Column with page title (link to page)
    '''
    name = 'title'

    def setCellProperties(self,
                          pageList: 'PageList',
                          item_index: ULC.UltimateListItem,
                          position: int,
                          page):
        if page.icon:
            image_index = pageList.imageList.add(page.icon)
        else:
            image_index = 0

        pageList.listCtrl.SetItemImage(item_index, image_index)
        pageList.listCtrl.SetItemHyperText(item_index, position)

    def getCellContent(self, page):
        return page.display_title

    def getTitle(self) -> str:
        return _('Title')


class ParentPageColumn(BaseColumn):
    '''
    Column with page parent path
    '''
    name = 'parent'

    def getCellContent(self, page):
        parent_page = page.parent
        if parent_page.parent:
            return parent_page.display_subpath + '/'

        return ''

    def getTitle(self) -> str:
        return _('Parent')


class TagsColumn(BaseColumn):
    '''
    Column with page tags
    '''
    name = 'tags'

    def getCellContent(self, page):
        return ', '.join(page.tags)

    def getTitle(self) -> str:
        return _('Tags')


class ModifyDateColumn(BaseColumn):
    '''
    Column with modify date of page
    '''
    name = 'moddate'

    def getCellContent(self, page):
        return page.datetime.strftime('%d.%m.%Y     %H:%M')

    def getTitle(self) -> str:
        return _('Modify date')


class PageList(wx.Panel):
    def __init__(self, parent: wx.Window, columns: List[BaseColumn]):
        super().__init__(parent)
        self._columns = columns
        self._defaultIcon = os.path.join(getImagesDir(), "page.png")
        self._imageList = ImageListCache(self._defaultIcon)

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
        self._listCtrl.AssignImageList(self._imageList.getImageList(),
                                       wx.IMAGE_LIST_SMALL)

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
                column.setCellProperties(self, item_index, n, page)

            data = PageData(page)
            self._listCtrl.SetItemPyData(item_index, data)

        self._listCtrl.Thaw()

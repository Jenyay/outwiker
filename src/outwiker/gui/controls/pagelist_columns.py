# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import List

import outwiker.gui.controls.ultimatelistctrl as ULC

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
            visible = (visible.lower() == 'true')
            column = self.createColumn(name, width, visible)
            columns.append(column)

        return columns

    @staticmethod
    def toString(columns: List['BaseColumn']) -> str:
        return ','.join(['{name}:{width}:{visible}'.format(name=col.name,
                                                           width=col.width,
                                                           visible=col.visible)
                         for col in columns])


class BaseColumn(metaclass=ABCMeta):
    '''
    Base class to manage columns
    '''
    SORT_NONE = 0
    SORT_NORMAL = 1
    SORT_INVERSE = 2

    def __init__(self,
                 width: int,
                 visible=True):
        self._width = width
        self._visible = visible
        self._sort_type = self.SORT_NONE
        self._column = None
        self._column_index = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def sort_type(self):
        return self._sort_type

    def set_sort_type(self, value, listCtrl: 'UltimateListCtrl'):
        self._sort_type = value

        assert self._column is not None
        assert self._column_index is not None

        if self._sort_type == self.SORT_NONE:
            self._column.SetText(self.getTitle())
        elif self._sort_type == self.SORT_NORMAL:
            self._column.SetText(self.getTitle() + '  ' + '\u25B2')
        elif self._sort_type == self.SORT_INVERSE:
            self._column.SetText(self.getTitle() + '  ' + '\u25BC')
        else:
            assert False

        listCtrl.SetColumn(self._column_index, self._column)

    def insertColumn(self,
                     listCtrl: 'UltimateListCtrl',
                     position: int):
        '''
        Add column
        '''
        index = listCtrl.InsertColumn(position, self.getTitle())
        listCtrl.SetColumnWidth(position, self.width)
        self._column_index = index
        self._column = listCtrl.GetColumn(index)

    def setCellProperties(self,
                          pageList: 'PageList',
                          item_index: ULC.UltimateListItem,
                          position: int,
                          page):
        pass

    @abstractmethod
    def getCellContent(self, page) -> str:
        pass

    @abstractmethod
    def getTitle(self) -> str:
        pass

    def sortFunction(self,
                     item1: ULC.UltimateListItem,
                     item2: ULC.UltimateListItem) -> int:
        page1 = item1.GetPyData().page
        page2 = item2.GetPyData().page

        content1 = self.getCellContent(page1).lower()
        content2 = self.getCellContent(page2).lower()

        return (content1 > content2) - (content1 < content2)

    def sortFunctionInverse(self,
                            item1: ULC.UltimateListItem,
                            item2: ULC.UltimateListItem) -> int:
        return -self.sortFunction(item1, item2)


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

    def sortFunction(self,
                     item1: ULC.UltimateListItem,
                     item2: ULC.UltimateListItem) -> int:
        page1 = item1.GetPyData().page
        page2 = item2.GetPyData().page

        content1 = page1.datetime
        content2 = page2.datetime

        return (content1 < content2) - (content1 > content2)

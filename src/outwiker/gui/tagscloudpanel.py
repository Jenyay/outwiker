# -*- coding: utf-8 -*-

from functools import reduce
from typing import List

import wx

from .guiconfig import TagsCloudConfig
from .tagscloud import TagsCloud
from .pagelistpopup import PageListPopup
from .tagspanelcontroller import TagsPanelController
from .controls.pagelist import (BaseColumn,
                                PageTitleColumn,
                                ParentPageColumn,
                                TagsColumn,
                                ModifyDateColumn)

PLP_HEADER_TITLE = 'title'
PLP_HEADER_PARENT = 'parent'
PLP_HEADER_TAGS = 'tags'
PLP_HEADER_MODDATE = 'moddate'


class TagsCloudPanel(wx.Panel):
    def __init__(self, parent, application):
        wx.Panel.__init__(self, parent)
        self._application = application
        self._tagscloud = TagsCloud(self)

        self._popupHeight = 200

        self._layout()

        self._controller = TagsPanelController(self, application)

    def _getPageListColumns(self) -> List[BaseColumn]:
        default = []
        default.append(PageTitleColumn(_('Title'), 200))
        default.append(ParentPageColumn(_('Parent'), 200))
        default.append(TagsColumn(_('Tags'), 200))
        default.append(ModifyDateColumn(_('Modify date'), 200))

        config = TagsCloudConfig(self._application.config)
        item_params = [item_str.strip()
                       for item_str
                       in config.popupHeaders.value]

        columns = []
        for item in item_params:
            try:
                name, width = item.split(':')
                width = int(width)
            except ValueError:
                return default

            if name == PLP_HEADER_TITLE:
                columns.append(PageTitleColumn(_('Title'), width))
            elif name == PLP_HEADER_PARENT:
                columns.append(ParentPageColumn(_('Parent'), width))
            elif name == PLP_HEADER_TAGS:
                columns.append(TagsColumn(_('Tags'), width))
            elif name == PLP_HEADER_MODDATE:
                columns.append(ModifyDateColumn(_('Modify date'), width))
            else:
                return default

        return columns

    def showPopup(self, pages):
        columns = self._getPageListColumns()
        width = reduce(lambda w, col: w + col.width, columns, 25)

        pageListPopup = PageListPopup(self,
                                      self._application.mainWindow,
                                      columns)

        pageListPopup.SetSize((width, self._popupHeight))
        pageListPopup.setPageList(pages)
        pageListPopup.Popup()

    def clearTags(self):
        self._tagscloud.clear()

    def clearMarks(self):
        self._tagscloud.clearMarks()

    def mark(self, tag, marked=True):
        self._tagscloud.mark(tag, marked)

    def setTags(self, tags):
        self._tagscloud.setTags(tags)

    def updateTagLabels(self):
        self._tagscloud.updateTagLabels()

    def _layout(self):
        mainSizer = wx.FlexGridSizer(1, 1, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self._tagscloud, 0, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(mainSizer)

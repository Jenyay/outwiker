# -*- coding: utf-8 -*-

from functools import reduce
from typing import List

import wx

from .guiconfig import TagsCloudConfig
from .tagscloud import TagsCloud
from .pagelistpopup import PageListPopup
from .tagspanelcontroller import TagsPanelController
from .controls.pagelist import (BaseColumn,
                                createColumnsFromString,
                                createDefaultColumns)


class TagsCloudPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._popupHeight = 200
        self._application = application

        self._createGUI()
        self._controller = TagsPanelController(self, application)

    def _getPageListColumns(self) -> List[BaseColumn]:
        config = TagsCloudConfig(self._application.config)
        try:
            columns = createColumnsFromString(config.popupHeaders.value)
        except ValueError:
            columns = createDefaultColumns()

        if not columns:
            columns = createDefaultColumns()

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

    def _createGUI(self):
        self._tagscloud = TagsCloud(self)
        mainSizer = wx.FlexGridSizer(1, 1, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self._tagscloud, 0, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(mainSizer)

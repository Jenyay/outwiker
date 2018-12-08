# -*- coding: utf-8 -*-

from typing import List

import wx

from .guiconfig import TagsConfig
from .tagscloud import TagsCloud
from .pagelistpopup import PageListPopup
from .tagspanelcontroller import TagsPanelController
from .controls.pagelist_columns import BaseColumn, ColumnsFactory


class TagsCloudPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application

        self._createGUI()
        self._controller = TagsPanelController(self, application)

    def _getPageListColumns(self) -> List[BaseColumn]:
        colFactory = ColumnsFactory()
        config = TagsConfig(self._application.config)
        try:
            columns = colFactory.createColumnsFromString(config.popupHeaders.value)
        except ValueError:
            columns = colFactory.createDefaultColumns()

        if not columns:
            columns = colFactory.createDefaultColumns()

        return columns

    def showPopup(self, pages):
        config = TagsConfig(self._application.config)
        columns = self._getPageListColumns()
        width = config.popupWidth.value
        height = config.popupHeight.value

        pageListPopup = PageListPopup(self, self._application.mainWindow)

        pageListPopup.setColumns(columns)
        pageListPopup.setPageList(pages)
        pageListPopup.sortByColumn(0)
        pageListPopup.SetSize((width, height))
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
        mainSizer.Add(self._tagscloud, 0, wx.EXPAND)
        self.SetSizer(mainSizer)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self._tagscloud.SetBackgroundColour(colour)

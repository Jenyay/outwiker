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
        self._pageListPopup = PageListPopup(self)
        self._pageListPopup.Bind(wx.EVT_CLOSE, handler=self._onPopupClose)

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

    def _onPopupClose(self, event):
        config = TagsConfig(self._application.config)
        self._savePopupSize(config)
        self._saveHeaders(config)
        event.Skip()

    def _saveHeaders(self, config: TagsConfig):
        columns = self._pageListPopup.getColumns()
        headers_str = ColumnsFactory.toString(columns)
        config.popupHeaders.value = headers_str

    def _savePopupSize(self, config: TagsConfig):
        width, height = self._pageListPopup.GetClientSize()
        config.popupWidth.value = width
        config.popupHeight.value = height

    def showPopup(self, pages):
        config = TagsConfig(self._application.config)
        columns = self._getPageListColumns()
        width = config.popupWidth.value
        height = config.popupHeight.value

        self._pageListPopup.setColumns(columns)
        self._pageListPopup.setPageList(pages)
        self._pageListPopup.sortByColumn(0)
        self._pageListPopup.SetClientSize((width, height))
        self._pageListPopup.Popup(self._application.mainWindow)

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

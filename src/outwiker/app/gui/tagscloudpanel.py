# -*- coding: utf-8 -*-

from typing import Collection, List

import wx

from outwiker.app.gui.tagspanelcontroller import TagsPanelController
from outwiker.app.gui.pagelistpopup import PageListPopup

from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.tagscloud import TagsCloud
from outwiker.gui.controls.pagelist_columns import BaseColumn, ColumnsFactory


class TagsCloudPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application

        self._createGUI()
        self._controller = TagsPanelController(self, application)
        self._pageListPopup = None

    def updateParamsFromConfig(self):
        config = TagsConfig(self._application.config)
        self._tagscloud.setFontSize(config.minFontSize.value, config.maxFontSize.value)
        self._tagscloud.setMode(config.tagsCloudMode.value)
        self._tagscloud.enableTooltips(config.enableTooltips.value)

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
        assert self._pageListPopup is not None
        config = TagsConfig(self._application.config)
        self._savePopupSize(config)
        self._saveHeaders(config)
        self._pageListPopup.Unbind(wx.EVT_CLOSE, handler=self._onPopupClose)
        self._pageListPopup.Destroy()
        self._pageListPopup = None
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
        assert self._pageListPopup is None

        config = TagsConfig(self._application.config)
        columns = self._getPageListColumns()
        width = config.popupWidth.value
        height = config.popupHeight.value

        self._pageListPopup = PageListPopup(self)
        self._pageListPopup.setColumns(columns)
        self._pageListPopup.setPageList(pages)
        self._pageListPopup.sortByColumn(0)
        self._pageListPopup.SetClientSize((width, height))
        self._pageListPopup.Popup(self._application.mainWindow)
        self._pageListPopup.Bind(wx.EVT_CLOSE, handler=self._onPopupClose)

    def clearTags(self):
        self._tagscloud.clear()

    def clearMarks(self):
        self._tagscloud.clearMarks()

    def mark(self, tag, marked=True):
        self._tagscloud.mark(tag, marked)

    def mark_list(self, tags: Collection[str], marked: bool = True):
        self._tagscloud.mark_list(tags, marked)

    def setTags(self, tags):
        self._tagscloud.setTags(tags)

    def _createGUI(self):
        config = TagsConfig(self._application.config)
        min_font_size = config.minFontSize.value
        max_font_size = config.maxFontSize.value
        mode = config.tagsCloudMode.value
        enable_tooltips = config.enableTooltips.value

        self._tagscloud = TagsCloud(
            self,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            mode=mode,
            enable_tooltips=enable_tooltips,
            enable_active_tags_filter=True
        )
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self._tagscloud, flag=wx.EXPAND)
        self.SetSizer(mainSizer)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self._tagscloud.SetBackgroundColour(colour)

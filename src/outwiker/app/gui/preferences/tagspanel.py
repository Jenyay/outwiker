# -*- coding: utf-8 -*-

import wx
from outwiker.gui.defines import TAGS_CLOUD_MODE_CONTINUOUS, TAGS_CLOUD_MODE_LIST

from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.controls.treebook2 import BasePrefPanel
from outwiker.gui.controls.pagelist_columns import ColumnsFactory


class TagsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)

        self._config = TagsConfig(application.config)
        self._createGui()
        self.LoadState()
        self.SetupScrolling()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        self._createFontGui(mainSizer)
        self._createModeGui(mainSizer)
        self._createTooltipsGui(mainSizer)
        self._createHeadersGui(mainSizer)
        self.SetSizer(mainSizer)

    def _createHeadersGui(self, mainsizer):
        text = wx.StaticText(self, label=_("Headers in the popup window: "))
        self._popupHeaders = wx.CheckListBox(self)
        self._popupHeaders.SetMinSize((250, 100))

        mainsizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mainsizer.Add(self._popupHeaders, 0, wx.ALL, border=2)

    def _createModeGui(self, mainsizer):
        modeSizer = wx.FlexGridSizer(cols=2)
        modeSizer.AddGrowableCol(0)

        modeLabel = wx.StaticText(self, label=_("Tags cloud view mode"))
        self._modeList = wx.ComboBox(self, choices=[_("As continuous text"), _("As list")], style=wx.CB_READONLY)
        self._modeList.SetMinSize((200, -1))

        modeSizer.Add(modeLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND| wx.ALL, border=2)
        modeSizer.Add(self._modeList, flag=wx.ALIGN_RIGHT | wx.EXPAND| wx.ALL, border=2)
        mainsizer.Add(modeSizer, 0, wx.EXPAND | wx.ALL, border=2)

    def _createFontGui(self, mainsizer):
        fontSizer = wx.FlexGridSizer(cols=2)
        fontSizer.AddGrowableCol(0)

        minFontSizeLabel = wx.StaticText(self, label=_("Minimum font size"))
        self._minFontSizeCtrl = wx.SpinCtrl(self, min=4, max=32)
        self._minFontSizeCtrl.SetMinSize((150, -1))

        maxFontSizeLabel = wx.StaticText(self, label=_("Maximum font size"))
        self._maxFontSizeCtrl = wx.SpinCtrl(self, min=4, max=32)
        self._maxFontSizeCtrl.SetMinSize((150, -1))

        fontSizer.Add(minFontSizeLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, border=2)
        fontSizer.Add(self._minFontSizeCtrl, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=2)

        fontSizer.Add(maxFontSizeLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, border=2)
        fontSizer.Add(self._maxFontSizeCtrl, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=2)

        mainsizer.Add(fontSizer, 0, wx.EXPAND | wx.ALL, border=2)

    def _createTooltipsGui(self, mainsizer):
        self._enableTooltips = wx.CheckBox(self, label=_("Show tooltips"))
        mainsizer.Add(self._enableTooltips, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)

    def _fillHeaders(self):
        factory = ColumnsFactory()
        text = self._config.popupHeaders.value
        try:
            columns = factory.createColumnsFromString(text)
        except ValueError:
            columns = factory.createDefaultColumns()

        if len(columns) != factory.typesCount:
            columns = factory.createDefaultColumns()

        self._popupHeaders.Clear()
        for col in columns:
            index = self._popupHeaders.Append(col.getTitle())
            self._popupHeaders.Check(index, col.visible)
            self._popupHeaders.SetClientData(index, col)

    def _saveHeadersState(self):
        columns = []
        for n in range(self._popupHeaders.GetCount()):
            col = self._popupHeaders.GetClientData(n)
            col.visible = self._popupHeaders.IsChecked(n) or col.name == "title"

            columns.append(col)

        factory = ColumnsFactory()
        text = factory.toString(columns)
        self._config.popupHeaders.value = text

    def LoadState(self):
        self._fillHeaders()
        self._minFontSizeCtrl.SetValue(self._config.minFontSize.value)
        self._maxFontSizeCtrl.SetValue(self._config.maxFontSize.value)
        self._modeList.SetSelection(1 if self._config.tagsCloudMode.value == TAGS_CLOUD_MODE_LIST else 0)
        self._enableTooltips.SetValue(self._config.enableTooltips.value)

    def Save(self):
        self._saveHeadersState()
        self._config.minFontSize.value = self._minFontSizeCtrl.GetValue()
        self._config.maxFontSize.value = self._maxFontSizeCtrl.GetValue()
        self._config.enableTooltips.value = self._enableTooltips.GetValue()

        if self._modeList.GetSelection() == 0:
            self._config.tagsCloudMode.value = TAGS_CLOUD_MODE_CONTINUOUS
        elif self._modeList.GetSelection() == 1:
            self._config.tagsCloudMode.value = TAGS_CLOUD_MODE_LIST

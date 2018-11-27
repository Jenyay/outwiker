# -*- coding: utf-8 -*-

import wx

from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.gui.controls.pagelist_columns import ColumnsFactory


class TagsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)

        self.ACTIONS_COMBOBOX_WIDTH = 300

        self._actions = [
            (_(u'Search pages with the tag'), TagsConfig.ACTION_SHOW_LIST),
            (_(u'Toggle tag selection'), TagsConfig.ACTION_MARK_TOGGLE),
        ]

        self._config = TagsConfig(application.config)
        self._createGui()
        self.SetupScrolling()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        self._createActionsGui(mainSizer)
        self._createHeadersGui(mainSizer)

        self.SetSizer(mainSizer)

    def _createActionsGui(self, mainsizer):
        actionsSizer = wx.FlexGridSizer(cols=2)
        actionsSizer.AddGrowableCol(0)

        leftClickActionLabel, self.leftClickActionCombo = self._createLabelAndComboBox(_(u'Left click on the tag'),
                                                                                       actionsSizer)
        middleClickActionLabel, self.middleClickActionCombo = self._createLabelAndComboBox(
            _(u'Middle click on the tag'), actionsSizer)

        mainsizer.Add(actionsSizer, 0, wx.EXPAND | wx.ALL, border=2)

    def _createHeadersGui(self, mainsizer):
        text = wx.StaticText(self, label=_('Headers in the popup window: '))
        self._popupHeaders = wx.CheckListBox(self)
        self._popupHeaders.SetMinSize((250, 100))

        self._fillHeaders()

        mainsizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mainsizer.Add(self._popupHeaders,
                      0,
                      wx.ALL,
                      border=2)

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

    def _fillActionsCombos(self):
        for action in self._actions:
            self.leftClickActionCombo.Append(action[0])
            self.middleClickActionCombo.Append(action[0])

        self.leftClickActionCombo.SetSelection(0)
        self.middleClickActionCombo.SetSelection(0)

        for n, action in enumerate(self._actions):
            if action[1] == self._config.leftClickAction.value:
                self.leftClickActionCombo.SetSelection(n)

            if action[1] == self._config.middleClickAction.value:
                self.middleClickActionCombo.SetSelection(n)

    def LoadState(self):
        self._fillActionsCombos()

    def _saveActionsState(self):
        leftClickAction = self.leftClickActionCombo.GetSelection()
        middleClickAction = self.middleClickActionCombo.GetSelection()

        assert leftClickAction >= 0 and leftClickAction < len(self._actions)
        assert middleClickAction >= 0 and middleClickAction < len(self._actions)

        self._config.leftClickAction.value = self._actions[leftClickAction][1]
        self._config.middleClickAction.value = self._actions[middleClickAction][1]

    def _saveHeadersState(self):
        columns = []
        for n in range(self._popupHeaders.GetCount()):
            col = self._popupHeaders.GetClientData(n)
            col.visible = self._popupHeaders.IsChecked(n) or col.name == 'title'

            columns.append(col)

        factory = ColumnsFactory()
        text = factory.toString(columns)
        self._config.popupHeaders.value = text

    def Save(self):
        self._saveActionsState()
        self._saveHeadersState()

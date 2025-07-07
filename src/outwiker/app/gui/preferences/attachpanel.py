# -*- coding: utf-8 -*-

import wx

from outwiker.gui.guiconfig import AttachConfig
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class AttachPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)

        self.ACTIONS_COMBOBOX_WIDTH = 200

        self._actions = [
            (_("Insert link to attachment"), AttachConfig.ACTION_INSERT_LINK),
            (_("Execute attachment"), AttachConfig.ACTION_OPEN),
        ]

        self._config = AttachConfig(application.config)
        self._createGui()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        self._createActionsGui(mainSizer)
        self._createShowHiddenDirsGui(mainSizer)

        self.SetSizer(mainSizer)

    def _createActionsGui(self, mainSizer):
        actionsSizer = wx.FlexGridSizer(cols=2)
        actionsSizer.AddGrowableCol(0)

        self.doubleClickActionCombo = self._createLabelAndComboBox(
            _("Double clicking or pressing Enter on an attached file"), actionsSizer
        )[1]

        self.doubleClickActionCombo.SetMinSize((self.ACTIONS_COMBOBOX_WIDTH, -1))
        mainSizer.Add(actionsSizer, 0, wx.EXPAND | wx.ALL, border=2)

    def _createShowHiddenDirsGui(self, mainSizer):
        self._showHiddenDirsCheckBox = wx.CheckBox(self, label=_("Show hidden folders"))
        mainSizer.Add(
            self._showHiddenDirsCheckBox,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=2,
        )

    def _fillActionsCombo(self):
        for action in self._actions:
            self.doubleClickActionCombo.Append(action[0])

        self.doubleClickActionCombo.SetSelection(0)

        for n, action in enumerate(self._actions):
            if action[1] == self._config.doubleClickAction.value:
                self.doubleClickActionCombo.SetSelection(n)

    def LoadState(self):
        self._fillActionsCombo()
        self._showHiddenDirsCheckBox.SetValue(self._config.showHiddenDirs.value)

    def _saveActionsState(self):
        doubleClickAction = self.doubleClickActionCombo.GetSelection()

        assert doubleClickAction >= 0 and doubleClickAction < len(self._actions)
        self._config.doubleClickAction.value = self._actions[doubleClickAction][1]
        self._config.showHiddenDirs.value = self._showHiddenDirsCheckBox.GetValue()

    def Save(self):
        self._saveActionsState()

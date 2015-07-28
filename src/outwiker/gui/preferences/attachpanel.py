# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import AttachConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class AttachPanel(BasePrefPanel):
    def __init__(self, parent):
        super (type(self), self).__init__ (parent)

        self.ACTIONS_COMBOBOX_WIDTH = 200

        self._actions = [
            (_(u'Insert link'), AttachConfig.ACTION_INSERT_LINK),
            (_(u'Open file'), AttachConfig.ACTION_OPEN),
        ]

        self._config = AttachConfig (Application.config)

        self._createGui()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        self._createActionsGui (mainSizer)

        self.SetSizer (mainSizer)


    def _createActionsGui (self, mainsizer):
        actionsSizer = wx.FlexGridSizer(cols=2)
        actionsSizer.AddGrowableCol(0)

        doubleClickActionLabel, self.doubleClickActionCombo = self._createLabelAndComboBox (
            _(u'Double click on an attached file'),
            actionsSizer)

        self.doubleClickActionCombo.SetMinSize((self.ACTIONS_COMBOBOX_WIDTH, -1))
        mainsizer.Add (actionsSizer, 0, wx.EXPAND | wx.ALL, border = 2)


    def _fillActionsCombo (self):
        for action in self._actions:
            self.doubleClickActionCombo.Append (action[0])

        self.doubleClickActionCombo.SetSelection (0)

        for n, action in enumerate (self._actions):
            if action[1] == self._config.doubleClickAction.value:
                self.doubleClickActionCombo.SetSelection (n)


    def LoadState(self):
        self._fillActionsCombo()


    def _saveActionsState (self):
        doubleClickAction = self.doubleClickActionCombo.GetSelection()

        assert doubleClickAction >= 0 and doubleClickAction < len (self._actions)
        self._config.doubleClickAction.value = self._actions[doubleClickAction][1]


    def Save (self):
        self._saveActionsState()

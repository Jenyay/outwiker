# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import AttachConfig


class AttachPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

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


    def _addControlsPairToSizer (self, sizer, label, control):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)


    def _createLabelAndComboBox (self, text, sizer):
        label = wx.StaticText (self, label = text)

        combobox = wx.ComboBox (self,
                                -1,
                                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        combobox.SetMinSize((self.ACTIONS_COMBOBOX_WIDTH, -1))

        self._addControlsPairToSizer (sizer, label, combobox)

        return (label, combobox)


    def _createActionsGui (self, mainsizer):
        actionsSizer = wx.FlexGridSizer(cols=2)
        actionsSizer.AddGrowableCol(0)

        doubleClickActionLabel, self.doubleClickActionCombo = self._createLabelAndComboBox (
            _(u'Double click on an attached file'),
            actionsSizer)
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

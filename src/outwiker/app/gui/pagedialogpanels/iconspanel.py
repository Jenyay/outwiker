# -*- coding: utf-8 -*-

import wx

from outwiker.gui.iconlistctrl import IconListCtrl
from outwiker.gui.controls.switchthemed import SwitchThemed
from outwiker.gui.theme import Theme


class IconsPanel(wx.Panel):
    """
    Class of the panel in the "Icon" tab.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._groupsButtonHeight = 32
        self._theme = Theme()
        self._createGui()

    def _createGui(self):
        self.iconsList = IconListCtrl(self, theme=self._theme)
        self.iconsList.SetMinSize((200, 150))

        # Control for selection icons group
        self.groupCtrl = SwitchThemed(self, self._theme)
        self.groupCtrl.SetButtonsHeight(self._groupsButtonHeight)

        self._layout()

    def _layout(self):
        iconSizer = wx.FlexGridSizer(cols=2)
        iconSizer.AddGrowableRow(0)
        iconSizer.AddGrowableCol(0, 1)
        iconSizer.AddGrowableCol(1, 3)
        iconSizer.Add(self.groupCtrl, 1, wx.ALL | wx.EXPAND, 2)
        iconSizer.Add(self.iconsList, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(iconSizer)
        self.Layout()

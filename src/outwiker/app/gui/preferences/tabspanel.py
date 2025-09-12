# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import TabsConfig
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class TabsPanel(BasePrefPanel):
    def __init__(self, parent, application: Application):
        super().__init__(parent)
        self._tabsConfig = TabsConfig(application.config)
        self._createGUI()
        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=2)
        main_sizer.AddGrowableCol(0)

        self._minTabWidthCtrl = self._createLabelAndSpin(_("Minimal tab width"), 40, 600, main_sizer)[1]
        self._maxTabWidthCtrl = self._createLabelAndSpin(_("Maximal tab width"), 50, 600, main_sizer)[1]

        self.SetSizer(main_sizer)
        self.Layout()

    def LoadState(self):
        self._minTabWidthCtrl.SetValue(self._tabsConfig.minTabWidth.value)
        self._maxTabWidthCtrl.SetValue(self._tabsConfig.maxTabWidth.value)

    def Save(self):
        min_tab_width = self._minTabWidthCtrl.GetValue()
        max_tab_width = self._maxTabWidthCtrl.GetValue()
        if min_tab_width > max_tab_width:
            min_tab_width = max_tab_width

        self._tabsConfig.minTabWidth.value = min_tab_width
        self._tabsConfig.maxTabWidth.value = max_tab_width

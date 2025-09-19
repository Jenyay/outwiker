# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.defines import TABS_MIN_FONT_SIZE, TABS_MAX_FONT_SIZE
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

        self._marginHorizontalCtrl = self._createLabelAndSpin(_("Horizontal margin"), 0, 24, main_sizer)[1]
        self._marginVerticalCtrl = self._createLabelAndSpin(_("Vertical margin"), 0, 24, main_sizer)[1]

        self._fontSizeComboBox = self._createLabelAndFontSize(
            _("Font size"),
            TABS_MIN_FONT_SIZE,
            TABS_MAX_FONT_SIZE,
            main_sizer,
        )[1]

        self.SetSizer(main_sizer)
        self.Layout()

    def LoadState(self):
        self._minTabWidthCtrl.SetValue(self._tabsConfig.minTabWidth.value)
        self._maxTabWidthCtrl.SetValue(self._tabsConfig.maxTabWidth.value)

        self._marginHorizontalCtrl.SetValue(self._tabsConfig.marginHorizontal.value)
        self._marginVerticalCtrl.SetValue(self._tabsConfig.marginVertical.value)

        font_size = self._tabsConfig.fontSize.value

        if (
            font_size is None
            or font_size < TABS_MIN_FONT_SIZE
            or font_size > TABS_MAX_FONT_SIZE
        ):
            self._fontSizeComboBox.SetSelection(0)
        else:
            index = 1 + font_size - TABS_MIN_FONT_SIZE
            self._fontSizeComboBox.SetSelection(index)

    def Save(self):
        min_tab_width = self._minTabWidthCtrl.GetValue()
        max_tab_width = self._maxTabWidthCtrl.GetValue()
        if min_tab_width > max_tab_width:
            min_tab_width = max_tab_width

        self._tabsConfig.minTabWidth.value = min_tab_width
        self._tabsConfig.maxTabWidth.value = max_tab_width

        self._tabsConfig.marginHorizontal.value = self._marginHorizontalCtrl.GetValue()
        self._tabsConfig.marginVertical.value = self._marginVerticalCtrl.GetValue()

        font_size_index = self._fontSizeComboBox.GetSelection()
        if font_size_index == 0:
            self._tabsConfig.fontSize.value = None
        else:
            font_size = font_size_index - 1 + TABS_MIN_FONT_SIZE
            self._tabsConfig.fontSize.value = font_size

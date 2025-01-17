# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences import configelements
from outwiker.gui.guiconfig import MainWindowConfig, GeneralGuiConfig
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class ColorsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._mainWindowConfig = MainWindowConfig(application.config)
        self._generalGuiConfig = GeneralGuiConfig(application.config)

        self._recentGuiColors = [
            wx.Colour(color_txt)
            for color_txt in self._generalGuiConfig.recentGuiColors.value
            if wx.Colour(color_txt).IsOk()
        ]

        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createMainWindowColorsGUI(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def _createMainWindowColorsGUI(self, main_sizer):
        sizer = self._createSection(main_sizer, _("Main window"))[1]

        # Panels background color
        self.panelsBackgroundColorPicker = self._createLabelAndColorPicker(
            _("Main panels background color"), sizer
        )[1]

        # Panels text color
        self.panelsTextColorPicker = self._createLabelAndColorPicker(
            _("Main panels text color"), sizer
        )[1]

    def LoadState(self):
        # Main panels
        self.panelsBackgroundColor = configelements.ColourElement(
            self._mainWindowConfig.mainPanesBackgroundColor,
            self.panelsBackgroundColorPicker,
        )

        self.panelsTextColor = configelements.ColourElement(
            self._mainWindowConfig.mainPanesTextColor, self.panelsTextColorPicker
        )

    def Save(self):
        # Main panels
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

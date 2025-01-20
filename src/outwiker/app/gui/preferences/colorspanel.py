# -*- coding: utf-8 -*-

import wx

# from outwiker.gui.preferences import configelements
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
        self.panelsBackgroundColorPicker = self._createLabelAndColorComboBox(
            _("Main panels background color"), sizer
        )[1]
        self.panelsBackgroundColorPicker.AddColors(self._recentGuiColors)

        # Panels text color
        self.panelsTextColorPicker = self._createLabelAndColorComboBox(
            _("Main panels text color"), sizer
        )[1]
        self.panelsTextColorPicker.AddColors(self._recentGuiColors)

    def LoadState(self):
        # Main panels
        self.panelsBackgroundColorPicker.SetSelectedColor(wx.Colour(self._mainWindowConfig.mainPanesBackgroundColor.value))
        self.panelsTextColorPicker.SetSelectedColor(wx.Colour(self._mainWindowConfig.mainPanesTextColor.value))

    def Save(self):
        # Main panels
        backgroundColor = self.panelsBackgroundColorPicker.GetSelectedColor()
        if backgroundColor is not None:
            self._mainWindowConfig.mainPanesBackgroundColor.value = backgroundColor.GetAsString(wx.C2S_HTML_SYNTAX)
        else:
            self._mainWindowConfig.mainPanesBackgroundColor.value = None

        textColor = self.panelsTextColorPicker.GetSelectedColor()
        if textColor is not None:
            self._mainWindowConfig.mainPanesTextColor.value = textColor.GetAsString(wx.C2S_HTML_SYNTAX)
        else:
            self._mainWindowConfig.mainPanesTextColor.value = None

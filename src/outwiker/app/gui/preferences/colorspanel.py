# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences import configelements
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.controls.treebook2 import BasePrefPanel


class ColorsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self.mainWindowConfig = MainWindowConfig(application.config)
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
        parent, sizer = self._createSection(main_sizer, _("Main window"))

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
            self.mainWindowConfig.mainPanesBackgroundColor,
            self.panelsBackgroundColorPicker,
        )

        self.panelsTextColor = configelements.ColourElement(
            self.mainWindowConfig.mainPanesTextColor, self.panelsTextColorPicker
        )

    def Save(self):
        # Main panels
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

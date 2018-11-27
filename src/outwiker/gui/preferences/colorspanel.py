# -*- coding: utf-8 -*-

import wx

from . import configelements
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


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

        self._createColorsGUI(main_sizer)

        self.SetSizer(main_sizer)

    def _createColorsGUI(self, main_sizer):
        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        # Panels background color
        self.panelsBackgroundColorLabel = wx.StaticText(
            self,
            label=_(u"Main panels background color"))

        self.panelsBackgroundColorPicker = wx.ColourPickerCtrl(self)

        colorsSizer.Add(self.panelsBackgroundColorLabel,
                        flag=wx.ALIGN_LEFT | wx.ALL,
                        border=2)
        colorsSizer.Add(self.panelsBackgroundColorPicker,
                        flag=wx.ALIGN_RIGHT | wx.ALL,
                        border=2)

        # Panels text color
        self.panelsTextColorLabel = wx.StaticText(
            self,
            label=_(u"Main panels text color"))

        self.panelsTextColorPicker = wx.ColourPickerCtrl(self)

        colorsSizer.Add(self.panelsTextColorLabel,
                        flag=wx.ALIGN_LEFT | wx.ALL,
                        border=2)
        colorsSizer.Add(self.panelsTextColorPicker,
                        flag=wx.ALIGN_RIGHT | wx.ALL,
                        border=2)

        main_sizer.Add(colorsSizer, flag=wx.EXPAND | wx.ALL, border=2)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        self.panelsBackgroundColor = configelements.ColourElement(
            self.mainWindowConfig.mainPanesBackgroundColor,
            self.panelsBackgroundColorPicker
        )

        self.panelsTextColor = configelements.ColourElement(
            self.mainWindowConfig.mainPanesTextColor,
            self.panelsTextColorPicker
        )

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

# -*- coding: utf-8 -*-

import os

import wx

from . import configelements
from outwiker.core.system import getImagesDir
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.controls.formatctrl import FormatCtrl
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class MainWindowPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self.mainWindowConfig = MainWindowConfig(application.config)
        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createTitleFormatGUI(main_sizer)
        self._createStatusbarGUI(main_sizer)
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

    def _createStatusbarGUI(self, main_sizer):
        self.statusbarVisibleCheckBox = wx.CheckBox(
            self,
            label=_('Show status panel')
        )
        main_sizer.Add(self.statusbarVisibleCheckBox,
                       flag=wx.ALIGN_LEFT | wx.ALL,
                       border=2)

    def _createTitleFormatGUI(self, main_sizer):
        """
        Создать элементы интерфейса, связанные с форматом заголовка
            главного окна
        """

        hints = [
            (u"{file}", _(u"Wiki file name")),
            (u"{page}", _(u"Page title")),
            (u"{subpath}", _(u"Relative path to current page")),
        ]

        self.titleFormatLabel = wx.StaticText(self,
                                              -1,
                                              _("Main window title format"))

        hintBitmap = wx.Bitmap(os.path.join(getImagesDir(), u"wand.png"))
        self.titleFormatText = FormatCtrl(
            self,
            self.mainWindowConfig.titleFormat.value,
            hints,
            hintBitmap)

        self.titleFormatSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.titleFormatSizer.Add(self.titleFormatLabel,
                                  0,
                                  wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                  2)

        self.titleFormatSizer.Add(self.titleFormatText,
                                  0,
                                  wx.ALL | wx.EXPAND,
                                  2)

        self.titleFormatSizer.AddGrowableCol(1)
        main_sizer.Add(self.titleFormatSizer, 1, wx.EXPAND, 0)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        # Формат заголовка страницы
        self.titleFormat = configelements.StringElement(
            self.mainWindowConfig.titleFormat,
            self.titleFormatText
        )

        self.statusbarVisible = configelements.BooleanElement(
            self.mainWindowConfig.statusbar_visible,
            self.statusbarVisibleCheckBox
        )

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
        self.titleFormat.save()
        self.statusbarVisible.save()
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

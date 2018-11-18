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

        self.SetSizer(main_sizer)

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

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.titleFormat.save()
        self.statusbarVisible.save()

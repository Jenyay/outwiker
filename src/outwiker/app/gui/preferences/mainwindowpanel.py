# -*- coding: utf-8 -*-

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.preferences import configelements
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.controls.formatctrl import FormatCtrl
from outwiker.gui.preferences.prefpanel import BasePrefPanel
from outwiker.gui.images import readImage
from outwiker.gui.defines import BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT


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
        self._createButtonsIconSizeGui(main_sizer)
        self._createStatusbarGUI(main_sizer)

        self.SetSizer(main_sizer)

    def _createStatusbarGUI(self, main_sizer):
        self.statusbarVisibleCheckBox = wx.CheckBox(self, label=_("Show status panel"))
        main_sizer.Add(
            self.statusbarVisibleCheckBox, flag=wx.ALIGN_LEFT | wx.ALL, border=2
        )

    def _createTitleFormatGUI(self, main_sizer):
        """
        Создать элементы интерфейса, связанные с форматом заголовка
            главного окна
        """

        hints = [
            ("{file}", _("Wiki file name")),
            ("{page}", _("Page title")),
            ("{subpath}", _("Relative path to current page")),
        ]

        self.titleFormatLabel = wx.StaticText(self, -1, _("Main window title format"))

        hintBitmap = readImage(
            getBuiltinImagePath("wand.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
        )
        self.titleFormatText = FormatCtrl(
            self, self.mainWindowConfig.titleFormat.value, hints, hintBitmap
        )

        self.titleFormatSizer = wx.FlexGridSizer(cols=2)
        self.titleFormatSizer.AddGrowableCol(1)
        self.titleFormatSizer.Add(
            self.titleFormatLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )

        self.titleFormatSizer.Add(self.titleFormatText, 0, wx.ALL | wx.EXPAND, 2)
        main_sizer.Add(self.titleFormatSizer, 1, wx.EXPAND, 0)

    def _createButtonsIconSizeGui(self, main_sizer):
        self._buttons_icon_size_items = [
            ("16 x 16", 16),
            ("20 x 20", 20),
            ("24 x 24", 24),
            ("32 x 32", 32),
            ("48 x 48", 48),
        ]

        sizer = wx.FlexGridSizer(cols=2)
        sizer.AddGrowableCol(1)

        self._buttonsIconSizeComboBox = self._createLabelAndComboBox(_("Buttons icon size (restart application required)"), sizer)[1]
        for title, size in self._buttons_icon_size_items:
            self._buttonsIconSizeComboBox.Append(title)

        main_sizer.Add(sizer, flag=wx.EXPAND)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        # Формат заголовка страницы
        self.titleFormat = configelements.StringElement(
            self.mainWindowConfig.titleFormat, self.titleFormatText
        )

        self.statusbarVisible = configelements.BooleanElement(
            self.mainWindowConfig.statusbar_visible, self.statusbarVisibleCheckBox
        )
        self._load_buttons_icon_size()

    def _load_buttons_icon_size(self):
        icon_size = self.mainWindowConfig.buttonsIconSize.value
        icon_size_index = 0
        for n, (title, size) in enumerate(self._buttons_icon_size_items):
            if size == icon_size:
                icon_size_index = n

        self._buttonsIconSizeComboBox.SetSelection(icon_size_index)

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.titleFormat.save()
        self.statusbarVisible.save()

        buttons_icon_size = self._buttons_icon_size_items[self._buttonsIconSizeComboBox.GetSelection()][1]
        self.mainWindowConfig.buttonsIconSize.value = buttons_icon_size

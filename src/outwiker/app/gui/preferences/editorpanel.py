# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences.prefpanel import BasePrefPanel
from outwiker.gui.preferences import configelements
from outwiker.gui.guiconfig import EditorConfig
from outwiker.core.config import FontOption


class EditorPanel(BasePrefPanel):
    """
    Панель с настройками, связанными с редактором
    """

    def __init__(self, parent, application):
        super().__init__(parent)

        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50

        self.__config = EditorConfig(application.config)
        self.__createGuiElements(self.__config)
        self.__do_layout()
        self.LoadState()
        self.SetupScrolling()

    def __createGuiElements(self, config):
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)
        self.lineNumbersCheckBox = wx.CheckBox(self, -1, _("Show line numbers"))
        self.tabUseSpacesCheckBox = wx.CheckBox(self, -1, _("Use spaces instead tabs"))
        self.tabWidthLabel = wx.StaticText(self, -1, _("Tab width"))

        self.tabWidthSpin = wx.SpinCtrl(
            self,
            -1,
            str(config.TAB_WIDTH_DEFAULT),
            min=self.MIN_TAB_WIDTH,
            max=self.MAX_TAB_WIDTH,
            style=wx.SP_ARROW_KEYS | wx.TE_AUTO_URL,
        )

        # Настройки для клавиш Home / End
        self.homeEndLabel = wx.StaticText(
            self, -1, _("Home / End keys moves the cursor \nto the beginning / end of ")
        )

        self.homeEndCombo = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.homeEndCombo.SetMinSize((200, -1))
        self.homeEndCombo.AppendItems([_("Line"), _("Paragraph")])

    def __do_layout(self):
        # Шрифт
        fontSizer = wx.FlexGridSizer(rows=1, cols=0, vgap=0, hgap=0)
        fontSizer.Add(self.fontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.Add(
            self.fontPicker, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2
        )
        fontSizer.AddGrowableRow(0)
        fontSizer.AddGrowableCol(1)

        # Размер табуляции
        tabWidthSizer = wx.FlexGridSizer(cols=2, rows=0, vgap=0, hgap=0)
        tabWidthSizer.Add(
            self.tabWidthLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )

        tabWidthSizer.Add(
            self.tabWidthSpin,
            0,
            wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            border=2,
        )
        tabWidthSizer.AddGrowableCol(1)

        # Поведение клавиш Home / End
        homeEndSizer = wx.FlexGridSizer(cols=2, rows=0, vgap=0, hgap=0)
        homeEndSizer.AddGrowableCol(0)
        homeEndSizer.AddGrowableCol(1)
        homeEndSizer.Add(
            self.homeEndLabel,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=2,
        )

        homeEndSizer.Add(
            self.homeEndCombo,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2,
        )

        # Добавление элементов в главный сайзер
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(fontSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(
            self.lineNumbersCheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        mainSizer.Add(self.tabUseSpacesCheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mainSizer.Add(tabWidthSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(homeEndSizer, 1, wx.EXPAND, 0)

        self.SetSizer(mainSizer)

    def LoadState(self):
        # Показывать ли номера строк?
        self.lineNumbers = configelements.BooleanElement(
            self.__config.lineNumbers, self.lineNumbersCheckBox
        )

        # Use spaces instead tabs
        self.tabUseSpaces = configelements.BooleanElement(
                self.__config.tabUseSpaces, self.tabUseSpacesCheckBox
                )

        # Шрифт для редактора
        fontOption = FontOption(
            self.__config.fontName,
            self.__config.fontSize,
            self.__config.fontIsBold,
            self.__config.fontIsItalic,
        )

        self.fontEditor = configelements.FontElement(fontOption, self.fontPicker)

        # Размер табуляции
        self.tabWidth = configelements.IntegerElement(
            self.__config.tabWidth,
            self.tabWidthSpin,
            self.MIN_TAB_WIDTH,
            self.MAX_TAB_WIDTH,
        )

        if self.__config.homeEndKeys.value == 0:
            self.homeEndCombo.SetSelection(0)
        else:
            self.homeEndCombo.SetSelection(1)

    def Save(self):
        self.lineNumbers.save()
        self.tabUseSpaces.save()
        self.fontEditor.save()
        self.tabWidth.save()
        self.__config.homeEndKeys.value = self.homeEndCombo.GetSelection()

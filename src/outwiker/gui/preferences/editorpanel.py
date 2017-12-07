# -*- coding: UTF-8 -*-

import wx

import configelements
from outwiker.core.application import Application
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.stcstyle import StcStyle
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.core.config import FontOption


class EditorPanel(BasePrefPanel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, parent):
        super(type(self), self).__init__(parent)

        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50

        self.__config = EditorConfig(Application.config)
        self.__createGuiElements(self.__config)
        self.__do_layout()
        self.LoadState()
        self._setScrolling()

    def __createGuiElements(self, config):
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)
        self.lineNumbersCheckBox = wx.CheckBox(self,
                                               -1,
                                               _("Show line numbers"))
        self.tabWidthLabel = wx.StaticText(self, -1, _("Tab width"))

        self.tabWidthSpin = wx.SpinCtrl(
            self,
            -1,
            str(config.TAB_WIDTH_DEFAULT),
            min=self.MIN_TAB_WIDTH,
            max=self.MAX_TAB_WIDTH,
            style=wx.SP_ARROW_KEYS | wx.TE_AUTO_URL)

        # Настройки для клавиш Home / End
        self.homeEndLabel = wx.StaticText(
            self,
            -1,
            _(u"Home / End keys moves the cursor \nto the beginning / end of ")
        )

        self.homeEndCombo = wx.ComboBox(self,
                                        -1,
                                        style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.homeEndCombo.SetMinSize((200, -1))
        self.homeEndCombo.AppendItems([_(u"Line"), _(u"Paragraph")])

        # Цвет шрифта
        self.fontColorLabel = wx.StaticText(self, label=_(u"Font color"))
        self.fontColorPicker = wx.ColourPickerCtrl(self)

        # Цвет фона
        self.backColorLabel = wx.StaticText(self, label=_(u"Background color"))
        self.backColorPicker = wx.ColourPickerCtrl(self)

        # Selected background text color
        self.selBackColorLabel = wx.StaticText(
            self,
            label=_(u"Background color of the selected text"))

        self.selBackColorPicker = wx.ColourPickerCtrl(self)

        # Margin background color
        self.marginBackColorLabel = wx.StaticText(
            self,
            label=_(u"Page margin background color")
        )

        self.marginBackColorPicker = wx.ColourPickerCtrl(self)

    def __do_layout(self):
        # Шрифт
        fontSizer = wx.FlexGridSizer(rows=1, cols=0, vgap=0, hgap=0)
        fontSizer.Add(self.fontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.Add(self.fontPicker,
                      1,
                      wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
                      2)
        fontSizer.AddGrowableRow(0)
        fontSizer.AddGrowableCol(1)

        # Цвета шрифта и фона
        colorsSizer = wx.FlexGridSizer(cols=2, rows=0, vgap=0, hgap=0)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        colorsSizer.Add(self.fontColorLabel,
                        0,
                        wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)

        colorsSizer.Add(self.fontColorPicker,
                        0,
                        wx.ALL | wx.ALIGN_RIGHT,
                        border=2)

        colorsSizer.Add(self.backColorLabel,
                        0,
                        wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)

        colorsSizer.Add(self.backColorPicker,
                        0,
                        wx.ALL | wx.ALIGN_RIGHT,
                        border=2)

        colorsSizer.Add(self.selBackColorLabel,
                        0,
                        wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)

        colorsSizer.Add(self.selBackColorPicker,
                        0,
                        wx.ALL | wx.ALIGN_RIGHT,
                        border=2)

        colorsSizer.Add(self.marginBackColorLabel,
                        0,
                        wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)

        colorsSizer.Add(self.marginBackColorPicker,
                        0,
                        wx.ALL | wx.ALIGN_RIGHT,
                        border=2)

        # Размер табуляции
        tabWidthSizer = wx.FlexGridSizer(cols=2, rows=0, vgap=0, hgap=0)
        tabWidthSizer.Add(self.tabWidthLabel,
                          0,
                          wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border=2)

        tabWidthSizer.Add(self.tabWidthSpin,
                          0,
                          wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
                          border=2)
        tabWidthSizer.AddGrowableCol(1)

        # Поведение клавиш Home / End
        homeEndSizer = wx.FlexGridSizer(cols=2, rows=0, vgap=0, hgap=0)
        homeEndSizer.AddGrowableCol(0)
        homeEndSizer.AddGrowableCol(1)
        homeEndSizer.Add(self.homeEndLabel,
                         0,
                         wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                         border=2)

        homeEndSizer.Add(self.homeEndCombo,
                         0,
                         wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                         border=2)

        # Добавление элементов в главный сайзер
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(fontSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(colorsSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.lineNumbersCheckBox,
                      0,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.Add(tabWidthSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(homeEndSizer, 1, wx.EXPAND, 0)

        self.SetSizer(mainSizer)

    def LoadState(self):
        # Показывать ли номера строк?
        self.lineNumbers = configelements.BooleanElement(
            self.__config.lineNumbers,
            self.lineNumbersCheckBox)

        # Шрифт для редактора
        fontOption = FontOption(self.__config.fontName,
                                self.__config.fontSize,
                                self.__config.fontIsBold,
                                self.__config.fontIsItalic)

        self.fontEditor = configelements.FontElement(fontOption,
                                                     self.fontPicker)

        # Размер табуляции
        self.tabWidth = configelements.IntegerElement(self.__config.tabWidth,
                                                      self.tabWidthSpin,
                                                      self.MIN_TAB_WIDTH,
                                                      self.MAX_TAB_WIDTH)

        if self.__config.homeEndKeys.value == 0:
            self.homeEndCombo.SetSelection(0)
        else:
            self.homeEndCombo.SetSelection(1)

        if StcStyle.checkColorString(self.__config.fontColor.value):
            self.fontColorPicker.SetColour(self.__config.fontColor.value)
        else:
            self.fontColorPicker.SetColour(wx.Color(0, 0, 0))

        if StcStyle.checkColorString(self.__config.backColor.value):
            self.backColorPicker.SetColour(self.__config.backColor.value)
        else:
            self.backColorPicker.SetColour(wx.Color(255, 255, 255))

        if StcStyle.checkColorString(self.__config.selBackColor.value):
            self.selBackColorPicker.SetColour(self.__config.selBackColor.value)
        else:
            self.selBackColorPicker.SetColour(wx.Color(192, 192, 192))

        if StcStyle.checkColorString(self.__config.marginBackColor.value):
            self.marginBackColorPicker.SetColour(
                self.__config.marginBackColor.value
            )
        else:
            self.marginBackColorPicker.SetColour(wx.Color(217, 217, 217))

    def Save(self):
        self.lineNumbers.save()
        self.fontEditor.save()
        self.tabWidth.save()
        self.__config.homeEndKeys.value = self.homeEndCombo.GetSelection()
        self.__config.fontColor.value = self.fontColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.__config.backColor.value = self.backColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.__config.selBackColor.value = self.selBackColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.__config.marginBackColor.value = self.marginBackColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

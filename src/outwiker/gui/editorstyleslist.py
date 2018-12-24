# -*- coding: utf-8 -*-

import wx


class EditorStylesList (wx.Panel):
    """
    Класс контрола для редактирования стилей редактора
    (цвет шрифта, жирность и т.п., цвет фона пока менять не будем)
    """

    def __init__(self, parent):
        super(EditorStylesList, self).__init__(parent)

        self.__createGui()
        self.__layout()
        self.__bind()

        self._styles = []

    def __createGui(self):
        self._stylesList = wx.ListBox(self, style=wx.LB_SINGLE)
        self._stylesList.SetMinSize((150, -1))

        self._colorPicker = wx.ColourPickerCtrl(self)
        self._bold = wx.CheckBox(self, label=_(u"Bold"))
        self._italic = wx.CheckBox(self, label=_(u"Italic"))
        self._underline = wx.CheckBox(self, label=_(u"Underline"))

    def __layout(self):
        styleSizer = wx.FlexGridSizer(cols=1)
        styleSizer.AddGrowableCol(0)
        styleSizer.Add(self._colorPicker, flag=wx.ALL | wx.EXPAND, border=2)
        styleSizer.Add(self._bold, flag=wx.ALL |
                       wx.ALIGN_CENTER_VERTICAL, border=2)
        styleSizer.Add(self._italic, flag=wx.ALL |
                       wx.ALIGN_CENTER_VERTICAL, border=2)
        styleSizer.Add(self._underline, flag=wx.ALL |
                       wx.ALIGN_CENTER_VERTICAL, border=2)

        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        mainSizer.Add(self._stylesList, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(styleSizer, flag=wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(mainSizer)
        self.Layout()

    def __bind(self):
        self._stylesList.Bind(
            wx.EVT_LISTBOX, self._onStyleSelect, self._stylesList)
        self._colorPicker.Bind(wx.EVT_COLOURPICKER_CHANGED,
                               self._onStyleChanged, self._colorPicker)
        self._bold.Bind(wx.EVT_CHECKBOX, self._onStyleChanged, self._bold)
        self._italic.Bind(wx.EVT_CHECKBOX, self._onStyleChanged, self._italic)
        self._underline.Bind(
            wx.EVT_CHECKBOX, self._onStyleChanged, self._underline)

    def _onStyleSelect(self, event):
        self._updateSelection()

    def _onStyleChanged(self, event):
        index = self._stylesList.GetSelection()

        if index >= 0:
            self._styles[index].fore = self._colorPicker.GetColour(
            ).GetAsString(wx.C2S_HTML_SYNTAX)
            self._styles[index].bold = self._bold.IsChecked()
            self._styles[index].italic = self._italic.IsChecked()
            self._styles[index].underline = self._underline.IsChecked()

    def _updateSelection(self):
        index = self._stylesList.GetSelection()

        if index >= 0:
            self._colorPicker.SetColour(self._styles[index].fore)
            self._bold.SetValue(self._styles[index].bold)
            self._italic.SetValue(self._styles[index].italic)
            self._underline.SetValue(self._styles[index].underline)

    def addStyle(self, title, style):
        """
        Добавить стиль в список
        title - название стиля
        style - экземпляр класса StcStyle
        """
        self._stylesList.Append(title)
        self._styles.append(style)

        if len(self._styles) == 1:
            self._stylesList.SetSelection(0)
            self._updateSelection()

    def getStyle(self, index):
        """
        Возвращает экземпляр класса StcStyle по номеру
        """
        assert index >= 0
        assert index < len(self._styles)

        return self._styles[index]

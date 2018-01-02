# -*- coding: utf-8 -*-

import wx
from wx.lib.scrolledpanel import ScrolledPanel


class BasePrefPanel(ScrolledPanel):
    def __init__(self, parent):
        style = wx.TAB_TRAVERSAL | wx.HSCROLL | wx.VSCROLL
        super(BasePrefPanel, self).__init__(parent, style=style)

    def LoadState(self):
        pass

    def Save(self):
        pass

    def _addControlsPairToSizer(self, sizer, label, control):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

    def _createLabelAndComboBox(self, text, sizer):
        label = wx.StaticText(self, label=text)
        combobox = wx.ComboBox(self,
                               -1,
                               style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self._addControlsPairToSizer(sizer, label, combobox)
        return(label, combobox)

    def _createLabelAndColorPicker(self, text, sizer):
        label = wx.StaticText(self, label=text)
        colorPicker = wx.ColourPickerCtrl(self)

        self._addControlsPairToSizer(sizer, label, colorPicker)
        return (label, colorPicker)

    def _createCheckBox(self, text, sizer):
        checkBox = wx.CheckBox(self, label=text)
        sizer.Add(checkBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        return checkBox

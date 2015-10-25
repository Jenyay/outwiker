# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import wx


class BasePrefPanel (wx.ScrolledWindow):
    __metaclass__ = ABCMeta


    def __init__ (self, parent):
        style = wx.TAB_TRAVERSAL | wx.HSCROLL | wx.VSCROLL
        super (BasePrefPanel, self).__init__ (parent, style=style)


    def _setScrolling (self):
        bottomElement = reduce (
            lambda left, right: right if (left is None or
                                          (right.GetPositionTuple()[1] + right.GetSizeTuple()[1]) >
                                          (left.GetPositionTuple()[1] + left.GetSizeTuple()[1])) else left,
            self.GetChildren(),
            None
        )

        if bottomElement is not None:
            btElementTop = bottomElement.GetPositionTuple()[1]
            btElementHeight = bottomElement.GetSizeTuple()[1]
            scrollHeight = btElementHeight
            scrollCount = (btElementTop + btElementHeight) / scrollHeight + 1

            self.SetScrollbars (0,
                                scrollHeight,
                                0,
                                scrollCount)


    @abstractmethod
    def LoadState (self):
        pass


    @abstractmethod
    def Save(self):
        pass


    def _addControlsPairToSizer (self, sizer, label, control):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)


    def _createLabelAndComboBox (self, text, sizer):
        label = wx.StaticText (self, label = text)
        combobox = wx.ComboBox (self,
                                -1,
                                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self._addControlsPairToSizer (sizer, label, combobox)
        return (label, combobox)


    def _createLabelAndColorPicker (self, text, sizer):
        label = wx.StaticText (self, label = text)
        colorPicker = wx.ColourPickerCtrl (self, style=wx.CLRP_SHOW_LABEL)

        self._addControlsPairToSizer (sizer, label, colorPicker)
        return (label, colorPicker)


    def _createCheckBox (self, text, sizer):
        checkBox = wx.CheckBox (self, label=text)
        sizer.Add (checkBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        return checkBox

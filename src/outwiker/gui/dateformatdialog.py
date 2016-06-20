# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.datetimeformatctrl import DateTimeFormatCtrl
from outwiker.core.system import getImagesDir


class DateFormatDialog(TestedDialog):
    def __init__(self, parent, message, title, initial=u""):
        super(DateFormatDialog, self).__init__(parent)

        self.__createGui()

        self._messageCtrl.SetLabel(message)
        self.SetTitle(title)
        self._formatCtrl.SetValue(initial)

        self.Fit()

    def __createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)
        mainSizer.AddGrowableRow(2)

        self._messageCtrl = wx.StaticText(self, -1, u'')
        hintBitmap = wx.Bitmap(os.path.join(getImagesDir(), u"wand.png"))
        self._formatCtrl = DateTimeFormatCtrl(self, hintBitmap)
        self._formatCtrl.SetMinSize((300, -1))

        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        mainSizer.Add(self._messageCtrl, 1, wx.ALL, border=2)
        mainSizer.Add(self._formatCtrl, 1, wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add(okCancel, 1, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=2)

        self.SetSizer(mainSizer)

    def GetValue(self):
        return self._formatCtrl.GetValue()

    def SetValue(self, value):
        return self._formatCtrl.SetValue(value)

    Value = property(GetValue, SetValue)

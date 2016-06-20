# -*- coding: UTF-8 -*-

from datetime import datetime

import wx

from outwiker.gui.controls.formatctrl import FormatCtrl
from outwiker.core.system import getOS


class DateTimeFormatCtrl(wx.Panel):
    def __init__(self, parent, buttonBitmap, initial=u''):
        """
        initial - Начальное значение в поле ввода
        """
        super(DateTimeFormatCtrl, self).__init__(parent)

        self._buttonBitmap = buttonBitmap
        self._initial = initial
        self._hints = [
            (u"%a", _(u"Abbreviated weekday name")),
            (u"%A", _(u"Full weekday name")),
            (u"%b", _(u"Abbreviated month name")),
            (u"%B", _(u"Full month name")),
            (u"%c", _(u"Appropriate date and time representation")),
            (u"%d", _(u"Day of the month as a decimal number [01,31]")),
            (u"%H", _(u"Hour(24-hour clock) as a decimal number [00,23]")),
            (u"%I", _(u"Hour(12-hour clock) as a decimal number [01,12]")),
            (u"%m", _(u"Month as a decimal number [01,12]")),
            (u"%M", _(u"Minute as a decimal number [00,59]")),
            (u"%p", _(u"AM or PM")),
            (u"%S", _(u"Second as a decimal number [00,61]")),
            (u"%x", _(u"Appropriate date representation")),
            (u"%X", _(u"Appropriate time representation")),
            (u"%y", _(u"Year without century [00,99]")),
            (u"%Y", _(u"Year with century")),
            (u"%%", _(u"A literal '%' character")),
        ]

        self._createGui()
        self.Bind(wx.EVT_TEXT,
                  handler=self._onChange,
                  source=self.dateTimeFormatCtrl.formatCtrl)
        self._updateExample()

    def _onChange(self, event):
        self._updateExample()

    def _createGui(self):
        self.dateTimeFormatCtrl = FormatCtrl(self,
                                             self._initial,
                                             self._hints,
                                             self._buttonBitmap)
        self.exampleText = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.exampleText.Enable(False)

        dateTimeSizer = wx.FlexGridSizer(cols=1)
        dateTimeSizer.AddGrowableCol(0)
        dateTimeSizer.Add(self.dateTimeFormatCtrl,
                          0,
                          wx.ALL | wx.EXPAND,
                          border=2)
        dateTimeSizer.Add(self.exampleText, 0, wx.ALL | wx.EXPAND, border=2)

        self.SetSizer(dateTimeSizer)

    def _updateExample(self):
        try:
            dateStr = unicode(datetime.now().strftime(
                self.GetValue().encode(getOS().filesEncoding)),
                getOS().filesEncoding)
            self.exampleText.SetValue(dateStr)
        except ValueError:
            pass

    def SetValue(self, value):
        self.dateTimeFormatCtrl.SetValue(value)

    def GetValue(self):
        return self.dateTimeFormatCtrl.GetValue()

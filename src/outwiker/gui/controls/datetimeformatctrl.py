# -*- coding: utf-8 -*-

from datetime import datetime

import wx

from outwiker.gui.controls.formatctrl import FormatCtrl


class DateTimeFormatCtrl(wx.Panel):
    def __init__(self, parent, buttonBitmap, initial=""):
        """
        initial - Начальное значение в поле ввода
        """
        super(DateTimeFormatCtrl, self).__init__(parent)

        self._buttonBitmap = buttonBitmap
        self._initial = initial
        self._hints = [
            ("%a", _("Abbreviated weekday name")),
            ("%A", _("Full weekday name")),
            ("%b", _("Abbreviated month name")),
            ("%B", _("Full month name")),
            ("%c", _("Appropriate date and time representation")),
            ("%d", _("Day of the month as a decimal number (01, 02, ..., 31)")),
            ("%H", _("Hour(24-hour clock) as a decimal number (00, 01, ..., 23)")),
            ("%I", _("Hour(12-hour clock) as a decimal number (01, 02, ..., 12)")),
            ("%m", _("Month as a decimal number (01, 02, ..., 12)")),
            ("%M", _("Minute as a decimal number (00, 01, ..., 59)")),
            ("%p", _("AM or PM")),
            ("%S", _("Second as a decimal number (00, 01, ..., 59)")),
            ("%x", _("Appropriate date representation")),
            ("%X", _("Appropriate time representation")),
            ("%y", _("Year without century (00, 01, ..., 99)")),
            ("%Y", _("Year with century")),
            ("%%", _("A literal '%' character")),
        ]

        self._createGui()
        self.Bind(
            wx.EVT_TEXT,
            handler=self._onChange,
            source=self.dateTimeFormatCtrl.formatCtrl,
        )
        self._updateExample()

    def _onChange(self, event):
        self._updateExample()

    def _createGui(self):
        self.dateTimeFormatCtrl = FormatCtrl(
            self, self._initial, self._hints, self._buttonBitmap
        )
        self.exampleText = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.exampleText.Enable(False)

        dateTimeSizer = wx.BoxSizer(wx.VERTICAL)
        dateTimeSizer.Add(self.dateTimeFormatCtrl, flag=wx.ALL | wx.EXPAND, border=2)
        dateTimeSizer.Add(self.exampleText, flag=wx.ALL | wx.EXPAND, border=2)

        self.SetSizer(dateTimeSizer)

    def _updateExample(self):
        try:
            dateStr = datetime.now().strftime(self.GetValue())
            self.exampleText.SetValue(dateStr)
        except ValueError:
            pass

    def SetValue(self, value):
        self.dateTimeFormatCtrl.SetValue(value)

    def GetValue(self):
        return self.dateTimeFormatCtrl.GetValue()

# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Union

import wx
import wx.adv

from outwiker.gui.testeddialog import TestedDialog


class DateTimeDialog(TestedDialog):
    def __init__(self,
                 parent: wx.Window,
                 title: str = '',
                 selectedDateTime: Union[datetime, None] = None):
        super().__init__(parent, title=title)
        self._createGUI()
        self.setDateTime(selectedDateTime)

    def setDateTime(self, selectedDateTime: Union[datetime, None]):
        self._selectedDateTime = (selectedDateTime
                                  if selectedDateTime is not None
                                  else datetime.now())
        self._calendarCtrl.SetDate(self._selectedDateTime)
        self._timeCtrl.SetValue(self._selectedDateTime)

    def getDateTime(self) -> datetime:
        date = self._calendarCtrl.GetDate()
        time = self._timeCtrl.GetValue()

        return datetime(date.year, date.month + 1, date.day,
                        time.hour, time.minute, time.second)

    def _createGUI(self):
        self._createControls()
        self._layoutControls()

    def _createControls(self):
        self._dateLabel = wx.StaticText(self, label=_('Date'))
        self._calendarCtrl = wx.adv.CalendarCtrl(
            self,
            style=wx.adv.CAL_SHOW_HOLIDAYS)

        self._timeLabel = wx.StaticText(self, label=_('Time'))
        self._timeCtrl = wx.adv.TimePickerCtrl(self)

    def _layoutControls(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        self._layoutCalendar(mainSizer)
        self._layoutTime(mainSizer)

        self._createOkCancelButtons(mainSizer)

        self.SetSizer(mainSizer)
        self.Fit()

    def _layoutCalendar(self, mainSizer):
        mainSizer.Add(self._dateLabel, flag=wx.ALL, border=2)
        mainSizer.Add(self._calendarCtrl, flag=wx.ALL | wx.EXPAND, border=2)

    def _layoutTime(self, mainSizer):
        timeSizer = wx.FlexGridSizer(cols=2)
        timeSizer.AddGrowableCol(1)
        timeSizer.Add(self._timeLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        timeSizer.Add(self._timeCtrl,
                      flag=wx.ALL | wx.ALIGN_RIGHT,
                      border=2)

        mainSizer.Add(timeSizer, flag=wx.ALL | wx.EXPAND, border=2)

    def _createOkCancelButtons(self, mainSizer):
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.Add(
            okCancel,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=8
        )

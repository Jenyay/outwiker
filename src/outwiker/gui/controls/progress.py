# -*- coding: utf-8 -*-

import wx


class ProgressWindow(wx.Frame):
    def __init__(self, parent: wx.Window,
                 title: str,
                 text: str):
        super().__init__(parent, style=wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR)
        self._title = title
        self._text = text
        self._parentTop = wx.GetTopLevelParent(parent)

        self._createGUI()
        self.ShowWindow()

    def _createGUI(self):
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)

        self._textLabel = wx.StaticText(self, label=self._text)
        sizer.Add(self._textLabel,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND | wx.ALL,
                  border=15)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

        self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)

    def ShowWindow(self):
        self._disabler = wx.WindowDisabler(self)
        self.CenterOnParent()
        self.Show()
        self.Raise()
        self.Restore()
        self.SetFocus()
        self.UpdatePulse()

    def UpdatePulse(self):
        self.Update()
        wx.SafeYield()

    def _onDestroy(self, event):
        del self._disabler
        if self._parentTop:
            self._parentTop.Enable()

        event.Skip()

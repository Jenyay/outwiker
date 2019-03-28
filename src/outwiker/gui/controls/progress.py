# -*- coding: utf-8 -*-

import wx


class ProgressWindow(wx.Frame):
    def __init__(self, parent: wx.Window,
                 title: str,
                 text: str):
        super().__init__(parent,
                         style=wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR)
        self._title = title
        self._text = text
        self._parentTop = wx.GetTopLevelParent(parent)
        self._updateCount = 0
        self._maxDotCount = 6

        self._createGUI()
        self.ShowWindow()

    def _createGUI(self):
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)

        self._titleLabel = wx.StaticText(self)
        self._titleLabel.SetLabelMarkup('<b>' + self._title + '</b>')

        self._textLabel = wx.StaticText(
            self,
            label=self._text + self._getTextSuffix(self._maxDotCount))

        sizer.Add(self._titleLabel,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.ALL,
                  border=10)
        sizer.Add(self._textLabel,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND | wx.ALL,
                  border=20)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()
        self.Update()

        self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)

    def ShowWindow(self):
        self._disabler = wx.WindowDisabler(self)
        self.CenterOnParent()
        self.Show()
        self.Restore()
        # self.SetFocus()
        self.UpdatePulse()
        self.Raise()

    def _getTextSuffix(self, updateCount):
        return '.' * (updateCount % (self._maxDotCount + 1))

    def UpdatePulse(self):
        self._updateCount += 1
        self._textLabel.SetLabel(
            self._text + self._getTextSuffix(self._updateCount))
        self.Update()
        wx.SafeYield()

    def _onDestroy(self, event):
        del self._disabler
        if self._parentTop:
            self._parentTop.Enable()

        event.Skip()

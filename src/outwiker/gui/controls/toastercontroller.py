# -*- coding: utf-8 -*-

from typing import Tuple

import wx

import wx.lib.agw.toasterbox as tb


class ToasterController(object):
    def __init__(self, parent):
        self._parent = parent

        self.DELAY_SEC = 10000
        self.COLOR_MESSAGE = '#66a3ff'

    def _calcPopupPos(self, width, height) -> Tuple[int, int]:
        rect = self._parent.GetRect()
        x = rect.GetRight() - width
        y = rect.GetBottom() - height

        return (x, y)

    def destroy(self):
        toasterbox = tb.ToasterBox(
            self._parent,
            tbstyle=tb.TB_COMPLEX,
            closingstyle=tb.TB_ONTIME | tb.TB_ONCLICK
        )
        toasterbox.CleanList()
        tb.winlist = []

    def showMessage(self, message):
        width = 250
        height = 100

        x, y = self._calcPopupPos(width, height)

        toasterbox = tb.ToasterBox(
            self._parent,
            tbstyle=tb.TB_COMPLEX,
            closingstyle=tb.TB_ONTIME | tb.TB_ONCLICK
        )
        toasterbox.SetPopupPauseTime(self.DELAY_SEC)
        toasterbox.SetPopupSize((width, height))
        toasterbox.SetPopupPosition((x, y))
        # toasterbox.SetPopupPositionByInt(3)

        parent = toasterbox.GetToasterBoxWindow()
        panel = InfoPanel(parent, message)
        parent.SetBackgroundColour(self.COLOR_MESSAGE)
        toasterbox.AddPanel(panel)
        toasterbox.Play()


class InfoPanel(wx.Panel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self._createGUI(parent, message)

    def _createGUI(self, parent, message):
        self._label = wx.StaticText(parent, label=message)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)

        sizer.Add(self._label, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.GetParent().Fit()

# -*- coding: utf-8 -*-

from typing import Tuple

import wx
import wx.lib.agw.toasterbox as tb

from outwiker.gui.theme import Theme


class ToasterController(object):
    def __init__(self, parent):
        self._parent = parent
        self._theme = Theme()

        self.DELAY_SEC = 7000

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

    def showError(self, message):
        title = _('Error')
        captionBackgroundColor = self._theme.colorErrorBackground
        captionForegroundColor = self._theme.colorErrorForeground
        self.showMessage(message,
                         title,
                         captionBackgroundColor,
                         captionForegroundColor)

    def showInfo(self, title, message):
        captionBackgroundColor = self._theme.colorInfoBackground
        captionForegroundColor = self._theme.colorInfoForeground
        self.showMessage(message,
                         title,
                         captionBackgroundColor,
                         captionForegroundColor)

    def showMessage(self,
                    message,
                    title,
                    captionBackgroundColor,
                    captionForegroundColor):
        width = 300
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

        parent = toasterbox.GetToasterBoxWindow()
        panel = InfoPanel(parent,
                          message, title,
                          captionBackgroundColor, captionForegroundColor)
        parent.SetBackgroundColour(self._theme.colorToasterBackground)
        toasterbox.AddPanel(panel)
        toasterbox.Play()


class InfoPanel(wx.Panel):
    def __init__(self,
                 parent,
                 message,
                 title,
                 captionBackgroundColor,
                 captionForegroundColor):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self._captionBackgroundColor = captionBackgroundColor
        self._captionForegroundColor = captionForegroundColor
        self._createGUI(parent, message, title)

    def _createGUI(self, parent, message, title):
        self._messageLabel = wx.StaticText(parent, label=message)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(1)

        captionPanel = self._createCaptionPanel(title)
        sizer.Add(captionPanel, flag=wx.EXPAND)
        sizer.Add(self._messageLabel, flag=wx.EXPAND | wx.ALL, border=4)
        self.SetSizer(sizer)
        self.GetParent().Fit()

    def _createCaptionPanel(self, caption):
        captionPanel = wx.Panel(self, style=wx.BORDER_SIMPLE)
        captionPanel.SetBackgroundColour(self._captionBackgroundColor)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)

        captionLabel = wx.StaticText(captionPanel, label=caption)
        captionPanel.SetForegroundColour(self._captionForegroundColor)
        sizer.Add(
            captionLabel,
            flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=4)

        captionPanel.SetSizer(sizer)
        return captionPanel

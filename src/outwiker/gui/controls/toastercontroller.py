# -*- coding: utf-8 -*-

from typing import Tuple

import wx
import wx.lib.agw.toasterbox as tb

from outwiker.gui.theme import Theme
from outwiker.gui.guiconfig import GeneralGuiConfig


class ToasterController:
    def __init__(self, parent, application):
        self._parent = parent
        self._application = application
        self._theme = self._application.theme
        self._config = GeneralGuiConfig(application.config)
        self._updateSettings()

        self._application.onPreferencesDialogClose += self._onPreferencesDialogClose

        # Use in tests, not for normal code
        self.counter = ToasterCounter()

    def _updateSettings(self):
        self.toaster_delay = self._config.toasterDelay.value

    def _onPreferencesDialogClose(self, dialog):
        self._updateSettings()

    def _calcPopupPos(self, width, height) -> Tuple[int, int]:
        rect = self._parent.GetRect()
        x = rect.GetRight() - width
        y = rect.GetBottom() - height

        return (x, y)

    def destroy(self):
        self._application.onPreferencesDialogClose -= self._onPreferencesDialogClose
        if not self._application.testMode:
            toasterbox = tb.ToasterBox(
                self._parent,
                tbstyle=tb.TB_COMPLEX,
                closingstyle=tb.TB_ONTIME | tb.TB_ONCLICK
            )
            toasterbox.CleanList()
            tb.winlist = []

    def showError(self, message):
        title = _('Error')
        captionBackgroundColor = self._theme.get(Theme.SECTION_NOTIFICATION, Theme.NOTIFICATION_ERROR_CAPTION_BACKGROUND_COLOR)
        captionForegroundColor = self._theme.get(Theme.SECTION_NOTIFICATION, Theme.NOTIFICATION_ERROR_CAPTION_TEXT_COLOR)
        self.showMessage(message,
                         title,
                         captionBackgroundColor,
                         captionForegroundColor)
        self.counter.incShowErrorCount()

    def showInfo(self, title, message):
        captionBackgroundColor = self._theme.get(Theme.SECTION_NOTIFICATION, Theme.NOTIFICATION_INFO_CAPTION_BACKGROUND_COLOR)
        captionForegroundColor = self._theme.get(Theme.SECTION_NOTIFICATION, Theme.NOTIFICATION_INFO_CAPTION_TEXT_COLOR)
        self.showMessage(message,
                         title,
                         captionBackgroundColor,
                         captionForegroundColor)
        self.counter.incShowInfoCount()

    def showMessage(self,
                    message,
                    title,
                    captionBackgroundColor,
                    captionForegroundColor):
        if not self._application.testMode:
            toasterbox = tb.ToasterBox(
                self._parent,
                tbstyle=tb.TB_COMPLEX,
                closingstyle=tb.TB_ONTIME | tb.TB_ONCLICK
            )

            parent = toasterbox.GetToasterBoxWindow()
            panel = InfoPanel(parent,
                              message, title,
                              captionBackgroundColor, captionForegroundColor)
            parent.SetBackgroundColour(self._theme.get(Theme.SECTION_NOTIFICATION, Theme.NOTIFICATION_BACKGROUND_COLOR))
            toasterbox.AddPanel(panel)
            toasterbox.SetPopupPauseTime(self.toaster_delay)

            width, height = panel.GetSize()
            toasterbox.SetPopupSize((width, height))
            x, y = self._calcPopupPos(width, height)
            toasterbox.SetPopupPosition((x, y))
            toasterbox.Play()

        self.counter.incShowCount()


class InfoPanel(wx.Panel):
    def __init__(self,
                 parent,
                 message,
                 title,
                 captionBackgroundColor,
                 captionForegroundColor):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self._margin = 4
        self._margin_bottom = 15
        self._width = 300
        self._height = 500
        self._captionBackgroundColor = captionBackgroundColor
        self._captionForegroundColor = captionForegroundColor
        self._createGUI(message, title)

    def _createGUI(self, message, title):
        self.SetMinClientSize((self._width, -1))

        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(1)

        captionPanel = self._createCaptionPanel(title)
        messageLabel = self._createMessageLabel(message)

        sizer.Add(captionPanel, flag=wx.EXPAND)
        sizer.Add(messageLabel, flag=wx.EXPAND | wx.ALL, border=self._margin)
        self.SetSizer(sizer)
        self.Fit()

    def _createMessageLabel(self, message: str) -> wx.StaticText:
        messageLabel = wx.StaticText(self, label=message + '\n')

        label_width = self._width - 2 * self._margin
        messageLabel.Wrap(label_width)

        width, height = messageLabel.GetBestSize()
        messageLabel.SetMinSize((self._width, height))

        messageLabel.Bind(wx.EVT_LEFT_DOWN, handler=self._onClick)
        return messageLabel

    def _onClick(self, event):
        event.ResumePropagation(1)
        event.Skip()

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
        captionLabel.Bind(wx.EVT_LEFT_DOWN, handler=self._onClick)
        captionPanel.Bind(wx.EVT_LEFT_DOWN, handler=self._onClick)
        return captionPanel


class ToasterCounter:
    def __init__(self):
        self.clear()

    def clear(self):
        self.showCount = 0
        self.showErrorCount = 0
        self.showInfoCount = 0

    def incShowCount(self):
        self.showCount += 1

    def incShowErrorCount(self):
        self.showErrorCount += 1

    def incShowInfoCount(self):
        self.showInfoCount += 1

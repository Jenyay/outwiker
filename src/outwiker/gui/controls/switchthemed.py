# -*- coding=utf-8 -*-

import wx
from wx.lib.newevent import NewCommandEvent
from wx.lib.scrolledpanel import ScrolledPanel

from stickybuttonthemed import StickyButtonThemed


SwitchEvent, EVT_SWITCH = NewCommandEvent()


class SwitchThemed(ScrolledPanel):
    def __init__(self, parent, theme=None):
        super(SwitchThemed, self).__init__(parent)
        self._theme = theme
        self._buttonsHeight = 40

        self._buttons = []
        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self.SetSizer(self._mainSizer)
        self.SetupScrolling()

    def _onButtonClick(self, event):
        current_button = event.GetEventObject()
        current_button.SetToggle(True)

        index = None

        for n, button in enumerate(self._buttons):
            if button != current_button:
                button.SetToggle(False)
            else:
                index = n

        if index is not None:
            self.Notify()

    def _updateMinWidth(self):
        minWidth = 30
        scrollWidth = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        for button in self._buttons:
            w, h = button.GetMinSize()
            if w > minWidth:
                minWidth = w

        self.SetMinSize((minWidth + scrollWidth, -1))

    def Notify(self):
        wx.PostEvent(self, SwitchEvent(self.GetId(), index=self.GetSelection()))

    def SetTheme(self, theme):
        map(lambda button: button.SetTheme(theme), self._buttons)

    def Append(self, label=u'', bitmap=None):
        button = StickyButtonThemed(self, label=label, bitmap=bitmap)

        if self._theme is not None:
            button.SetTheme(self._theme)

        w, h = button.GetMinSize()
        button.SetMinSize((w, self._buttonsHeight))
        button.SetToggleShift(0, 0)
        button.SetRoundRadius(0)
        button.SetColorBorder(wx.Colour(255, 255, 255))
        button.Bind(wx.EVT_BUTTON, handler=self._onButtonClick)

        if len(self._buttons) == 0:
            button.SetToggle(True)

        self._buttons.append(button)
        self._mainSizer.Add(button, flag=wx.EXPAND | wx.ALL, border=0)
        self._updateMinWidth()
        self.Layout()

    def GetSelection(self):
        for n, button in enumerate(self._buttons):
            if button.GetToggle():
                return n

        return wx.NOT_FOUND

    def SetSelection(self, index):
        assert index >= 0
        assert index < len(self._buttons)

        map(lambda button: button.SetToggle(False), self._buttons)
        self._buttons[index].SetToggle(True)
        self._buttons[index].SetFocus()
        self.Notify()

    def GetButtonsHeight(self):
        return self._buttonsHeight

    def SetButtonsHeight(self, height):
        self._buttonsHeight = height
        map(lambda button: button.SetMinSize((-1, self._buttonsHeight)),
            self._buttons)
        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(200, 400))
        self.switch = SwitchThemed(self)
        self.switch.Bind(EVT_SWITCH, self._onSwitch)

        for n in range(20):
            self.switch.Append(u'Кнопка {}'.format(n))

        self.switch.SetSelection(4)

    def _onSwitch(self, event):
        print event.index
        print self.switch.GetSelection()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'SwitchThemed Test')
    frame.Show()
    app.MainLoop()

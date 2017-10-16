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
            wx.PostEvent(self, SwitchEvent(self.GetId(), index=index))

    def SetTheme(self, theme):
        map(lambda button: button.SetTheme(theme), self._buttons)

    def AddItem(self, label=u'', bitmap=None):
        button = StickyButtonThemed(self, label=label, bitmap=bitmap)
        button.SetMinSize((-1, self._buttonsHeight))
        button.SetToggleShift(0, 0)
        button.SetRoundRadius(0)
        button.SetColorBorder(wx.Colour(255, 255, 255))
        button.Bind(wx.EVT_BUTTON, handler=self._onButtonClick)

        if self._theme is not None:
            button.SetTheme(self._theme)

        if len(self._buttons) == 0:
            button.SetToggle(True)

        self._buttons.append(button)
        self._mainSizer.Add(button, flag=wx.EXPAND | wx.ALL, border=0)
        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(200, 400))
        switch = SwitchThemed(self)
        switch.Bind(EVT_SWITCH, self._onSwitch)

        for n in range(20):
            switch.AddItem(u'Кнопка {}'.format(n))

    def _onSwitch(self, event):
        print event.index


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'SwitchThemed Test')
    frame.Show()
    app.MainLoop()

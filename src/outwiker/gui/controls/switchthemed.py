# -*- coding=utf-8 -*-

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from togglebuttonthemed import ToggleButtonThemed


class SwitchThemed(ScrolledPanel):
    def __init__(self, parent, theme=None):
        super(SwitchThemed, self).__init__(parent)
        self._theme = theme
        self._buttons = []
        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self.SetSizer(self._mainSizer)

    def _onButtonClick(self, event):
        button = event.GetEventObject()
        if not button.GetToggle():
            button.SetToggle(True)

    def SetTheme(self, theme):
        map(lambda button: button.SetTheme(theme), self._buttons)

    def AddItem(self, label=u'', bitmap=None):
        button = ToggleButtonThemed(self, label=label, bitmap=bitmap)
        button.Bind(wx.EVT_BUTTON, handler=self._onButtonClick)

        if self._theme is not None:
            button.SetTheme(self._theme)

        if len(self._buttons) == 0:
            button.SetToggle(True)

        self._buttons.append(button)
        self._mainSizer.Add(button, flag=wx.EXPAND)
        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(200, 400))
        switch = SwitchThemed(self)

        for n in range(20):
            switch.AddItem(u'Кнопка {}'.format(n))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'SwitchThemed Test')
    frame.Show()
    app.MainLoop()
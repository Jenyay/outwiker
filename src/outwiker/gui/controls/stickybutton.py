# -*- coding: utf-8 -*-

import wx

from togglebutton import ToggleButton


class StickyButton(ToggleButton):
    def OnLeftDown(self, event):
        if self.GetToggle():
            event.Skip()
        else:
            super(StickyButton, self).OnLeftDown(event)

    def OnKeyUp(self, event):
        if self.GetToggle():
            event.Skip()
        else:
            super(StickyButton, self).OnKeyUp(event)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
        panel = wx.Panel(self)

        # Build a bitmap button and a normal one
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))

        btn = StickyButton(panel, -1, bmp, label=u'adsfasdf', pos=(10, 10))
        btn.SetSize((150, 75))

        btn2 = StickyButton(panel, -1, bmp, label=u'adsfasdf', pos=(10, 110), align=wx.ALIGN_CENTER)
        btn2.SetSize((150, 75))

        btn3 = StickyButton(panel, -1, bmp, label=u'adsfasdfadsf', pos=(10, 210), align=wx.ALIGN_CENTER)
        btn3.SetSize(btn3.GetMinSize())
        btn3.SetRoundRadius(0)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'StickyButton Test')
    frame.Show()
    frame.SetSize((500, 600))
    app.MainLoop()

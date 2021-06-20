# -*- coding: utf-8 -*-

from .evthandler import EvtHandler


class Window(EvtHandler):
    def __init__(self):
        super(Window, self).__init__()

        self.Enabled = True

    def GetSize(self):
        return(0, 0)

    def GetClientSize(self):
        return(0, 0)

    def SetSizeWH(self, width, height):
        pass

    def SetClientSize(self, width, height):
        pass

    def Enable(self, enable):
        self.Enabled = enable

    def Disabled(self):
        self.Enabled = False

    def IsEnabled(self):
        return self.Enabled

    def SetFocus(self):
        pass

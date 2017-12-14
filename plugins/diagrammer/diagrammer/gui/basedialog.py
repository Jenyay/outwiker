# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class BaseDialog (TestedDialog):
    def __init__ (self, parent):
        super (BaseDialog, self).__init__ (
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)


    def Destroy (self):
        self.GetSizer().Clear (True)
        super (BaseDialog, self).Destroy()

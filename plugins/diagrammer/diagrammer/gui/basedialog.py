# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.dialogs.testeddialog import TestedDialog


class BaseDialog(TestedDialog):
    def __init__(self, parent: wx.Window):
        super().__init__(parent,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

    def Destroy(self):
        self.GetSizer().Clear(True)
        super(BaseDialog, self).Destroy()

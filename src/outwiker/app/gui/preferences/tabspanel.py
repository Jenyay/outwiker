# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class TabsPanel(BasePrefPanel):
    def __init__(self, parent, application: Application):
        super().__init__(parent)
        self._createGUI()
        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)


        self.SetSizer(main_sizer)
        self.Layout()

    def LoadState(self):
        pass

    def Save(self):
        pass

# coding: utf-8

import wx

from outwiker.app.gui.pagedialogpanels.iconspanel import IconsPanel
from outwiker.gui.controls.popupwindow import PopupWindow


class IconsListPopup(PopupWindow):
    def __init__(self, parent):
        super().__init__(parent)

    def createGUI(self):
        self._iconsPanel = IconsPanel(self)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._iconsPanel, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    @property
    def iconsPanel(self):
        return self._iconsPanel

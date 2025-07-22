import wx

from outwiker.gui.defines import CONTROLS_MARGIN


class MarginSizer(wx.FlexGridSizer):
    def __init__(self):
        super().__init__(cols=1, hgap=0, vgap=0)
        self.AddGrowableCol(0)
        self.AddGrowableRow(0)

    def Add(self, item: wx.Object):
        super().Add(item, flag=wx.EXPAND | wx.ALL, border=CONTROLS_MARGIN)

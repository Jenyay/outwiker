from typing import List, Optional
import wx
import wx.adv

_ = globals().get("_", lambda txt: txt)


class ColorComboBox(wx.adv.OwnerDrawnComboBox):
    def __init__(self, parent):
        super().__init__(parent, style=wx.CB_READONLY)

        self.Append("default", None)
        self.Append("select color", None)
        self._oldSelection = 0
        self.SetSelection(self._oldSelection)

        self.Bind(wx.EVT_COMBOBOX, handler=self._onSelection)

    def _onSelection(self, event):
        index = self.GetSelection()
        if index != self.GetCount() - 1:
            self._oldSelection = self.GetSelection()
            return

        newcolor = wx.GetColourFromUser(wx.GetTopLevelParent(self), None)
        if newcolor.IsOk():
            self.Insert("", 1, newcolor)
            self._oldSelection = 1

        self.SetSelection(self._oldSelection)

    def AddColors(self, colors: List[wx.Colour]):
        for color in colors:
            self.Insert("", self.GetCount() - 1, color)

    def InsertColor(self, index: int, color: wx.Colour):
        assert index >= 1
        self.Insert("", index, color)

    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            return

        if item == 0:
            dc.DrawText(_("Default color"), rect.x + 5, rect.y + 2)
        elif item == self.GetCount() - 1:
            dc.DrawText(_("Select color..."), rect.x + 5, rect.y + 2)
        else:
            color = self.GetClientData(item)
            dc.SetBrush(wx.Brush(color))
            dc.SetPen(wx.Pen(color))
            dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

            if flags & wx.adv.ODCB_PAINTING_SELECTED:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.Pen(wx.BLACK, 1, wx.PENSTYLE_DOT))
                dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

    def GetSelectedColor(self) -> Optional[wx.Colour]:
        return self.GetClientData(self.GetSelection())

    def GetColors(self) -> List[wx.Colour]:
        return [self.GetClientData(index) for index in range(1, self.GetCount() - 1)]

    def FindColor(self, color: wx.Colour) -> Optional[int]:
        index = None
        for n in range(1, self.GetCount() - 1):
            current_color = self.GetClientData(n)
            if current_color is not None and current_color == color:
                index = n
                break
        return index

    def OnMeasureItem(self, item):
        return 20

    def OnMeasureItemWidth(self, item):
        return 150


if __name__ == "__main__":

    class MyApp(wx.App):
        def OnInit(self):
            self.frame = MyFrame(None, title="Color ComboBox Example")
            self.frame.Show(True)
            return True

    class MyFrame(wx.Frame):
        def __init__(self, *args, **kw):
            super(MyFrame, self).__init__(*args, **kw)
            panel = wx.Panel(self)

            colors = [
                wx.Colour(255, 0, 0),
                wx.Colour(0, 255, 0),
                wx.Colour(0, 0, 255),
                wx.Colour(255, 255, 0),
                wx.Colour(0, 255, 255),
                wx.Colour(255, 0, 255),
            ]

            self.combo = ColorComboBox(panel)
            self.combo.AddColors(colors)

            panel_sizer = wx.BoxSizer(wx.VERTICAL)
            panel_sizer.Add(self.combo, 0, wx.ALL | wx.EXPAND, 5)
            panel.SetSizer(panel_sizer)

            frame_sizer = wx.BoxSizer(wx.VERTICAL)
            frame_sizer.Add(panel, 1, wx.ALL | wx.EXPAND, 5)
            self.SetSizerAndFit(frame_sizer)

    app = MyApp(False)
    app.MainLoop()

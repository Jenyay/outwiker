from typing import List, Optional
import wx
import wx.adv

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

    def _drawText(self, text: str, dc: wx.DC, rect: wx.Rect):
        text_height = dc.GetTextExtent(text).GetHeight()
        y = (rect.GetHeight() - text_height) // 2
        dc.DrawText(text, rect.x + 5, rect.y + y)

    def OnDrawItem(self, dc: wx.DC, rect: wx.Rect, item: int, flags: int):
        if item == wx.NOT_FOUND:
            return

        if item == 0:
            self._drawText(_("Default color"), dc, rect)
        elif item == self.GetCount() - 1:
            self._drawText(_("Select color..."), dc, rect)
        else:
            color = self.GetClientData(item)
            dc.SetBrush(wx.Brush(color))
            dc.SetPen(wx.Pen(color))
            dc.DrawRectangle(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)

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
        return 24

    def OnMeasureItemWidth(self, item):
        return 150


if __name__ == "__main__":
    global _
    _ = lambda txt: txt

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

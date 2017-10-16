# -*- coding: utf-8 -*-

import wx
from wx.lib.buttons import ThemedGenBitmapTextToggleButton


class ToggleButton(ThemedGenBitmapTextToggleButton):
    def __init__(self,
                 parent,
                 id=-1,
                 bitmap=wx.NullBitmap,
                 label='',
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=0,
                 validator=wx.DefaultValidator,
                 name="togglebutton",
                 align=wx.ALIGN_LEFT):
        super(ToggleButton, self).__init__(parent, id, bitmap,
                                           label, pos, size,
                                           style, validator, name)
        self.colorNormal = wx.Colour(255, 255, 255)
        self.colorToggled = wx.Colour(144, 195, 212)
        self.colorShadow = wx.Colour(200, 200, 200)
        self.colorBorder = wx.Colour(0, 0, 0)
        self.colorBorderToggled = wx.Colour(0, 0, 255)
        self.colorTextNormal = wx.Colour(0, 0, 0)
        self.colorTextDisabled = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.colorTextToggled = wx.Colour(0, 0, 0)
        self.toggleShiftX = 2
        self.toggleShiftY = 2
        self.roundRadius = 2
        self.align = align
        self.padding = 8
        self.marginImage = 4

        self._updateMinSize()

    def _updateMinSize(self):
        contentWidth = self.GetContentWidth()
        self.SetMinSize((contentWidth + self.padding * 2 + self.toggleShiftX,
                         -1))

    def GetColorNormal(self):
        return self.colorNormal

    def SetColorNormal(self, color):
        self.colorNormal = color
        self.Refresh()

    def GetColorToggled(self):
        return self.colorToggled

    def SetColorToggled(self, color):
        self.colorToggled = color
        self.Refresh()

    def GetColorShadow(self):
        return self.colorShadow

    def SetColorShadow(self, color):
        self.colorShadow = color
        self.Refresh()

    def GetColorBorder(self):
        return self.colorBorder

    def SetColorBorder(self, color):
        self.colorBorder = color
        self.Refresh()

    def GetColorBorderToggled(self):
        return self.colorBorderToggled

    def SetColorBorderToggled(self, color):
        self.colorBorderToggled = color
        self.Refresh()

    def GetColorTextNormal(self):
        return self.colorTextNormal

    def SetColorTextNormal(self, color):
        self.colorTextNormal = color
        self.Refresh()

    def GetColorTextDisabled(self):
        return self.colorTextDisabled

    def SetColorTextDisabled(self, color):
        self.colorTextDisabled = color
        self.Refresh()

    def GetColorTextToggled(self):
        return self.colorTextToggled

    def SetColorTextToggled(self, color):
        self.colorTextToggled = color
        self.Refresh()

    def GetAlign(self):
        return self.align

    def SetAlign(self, align):
        self.align = align
        self.Refresh()

    def GetToggleShift(self):
        return (self.toggleShiftX, self.toggleShiftY)

    def SetToggleShift(self, shiftX, shiftY):
        self.toggleShiftX = shiftX
        self.toggleShiftY = shiftY
        self.Refresh()

    def GetRoundRadius(self):
        return self.roundRadius

    def SetRoundRadius(self, radius):
        self.roundRadius = radius
        self.Refresh()

    def GetPadding(self):
        return self.padding

    def SetPadding(self, padding):
        self.padding = padding
        self._updateMinSize()
        self.Refresh()

    def GetMarginImage(self):
        return self.marginImage

    def SetMarginImage(self, margin):
        self.marginImage = margin
        self._updateMinSize()
        self.Refresh()

    def DrawFocusIndicator(self, dc, w, h):
        bw = self.bezelWidth
        textClr = self.GetForegroundColour()
        focusIndPen = wx.Pen(textClr, 1, wx.USER_DASH)
        focusIndPen.SetDashes([1, 1])
        focusIndPen.SetCap(wx.CAP_BUTT)

        if wx.Platform == "__WXMAC__":
            dc.SetLogicalFunction(wx.XOR)
        else:
            focusIndPen.SetColour(self.focusClr)
            dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(focusIndPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        if self.GetToggle():
            shiftX = self.toggleShiftX
            shiftY = self.toggleShiftY
        else:
            shiftX = 0
            shiftY = 0

        dc.DrawRoundedRectangle(bw+2 + shiftX,
                                bw+2 + shiftY,
                                w-bw*2-5 - self.toggleShiftX,
                                h-bw*2-5 - self.toggleShiftY,
                                self.roundRadius)

        dc.SetLogicalFunction(wx.COPY)

    def DrawBezel(self, dc, x1, y1, x2, y2):
        width_full = x2 - x1
        height_full = y2 - y1

        rect_width = width_full - self.toggleShiftX
        rect_height = height_full - self.toggleShiftY

        rect_x0 = 0 if not self.GetToggle() else self.toggleShiftX
        rect_y0 = 0 if not self.GetToggle() else self.toggleShiftY

        # Draw shadow
        brushShadow = wx.Brush(self.colorShadow)
        penShadow = wx.Pen(self.colorShadow)

        dc.SetBrush(brushShadow)
        dc.SetPen(penShadow)
        dc.DrawRoundedRectangle(self.toggleShiftX, self.toggleShiftY,
                                rect_width, rect_height,
                                self.roundRadius)

        # Draw button
        color = self.colorToggled if self.GetToggle() else self.colorNormal
        colorBorder = self.colorBorderToggled if self.GetToggle() else self.colorBorder
        brush = wx.Brush(color)
        pen = wx.Pen(colorBorder)

        dc.SetBrush(brush)
        dc.SetPen(pen)
        dc.DrawRoundedRectangle(rect_x0, rect_y0,
                                rect_width, rect_height,
                                self.roundRadius)

        dc.SetBrush(wx.NullBrush)

    def _getBitmap(self):
        bmp = self.bmpLabel
        if bmp is not None:
            # if the bitmap is used
            if self.bmpDisabled and not self.IsEnabled():
                bmp = self.bmpDisabled
            if self.bmpFocus and self.hasFocus:
                bmp = self.bmpFocus
            if self.bmpSelected and not self.up:
                bmp = self.bmpSelected

        return bmp

    def GetContentWidth(self):
        bmp = self._getBitmap()
        if bmp is not None:
            bw = bmp.GetWidth()
        else:
            # no bitmap -> size is zero
            bw = 0

        label = self.GetLabel()
        dc = wx.WindowDC(self)
        dc.SetFont(self.GetFont())

        # size of text
        tw, th = dc.GetTextExtent(label)

        contentWidth = bw + tw + self.marginImage
        return contentWidth

    def DrawLabel(self, dc, width, height, dx=0, dy=0):
        if self.IsEnabled() and self.GetToggle():
            dc.SetTextForeground(self.colorTextToggled)
        elif self.IsEnabled():
            dc.SetTextForeground(self.colorTextNormal)
        else:
            dc.SetTextForeground(self.colorTextDisabled)

        bmp = self._getBitmap()
        if bmp is not None:
            bw, bh = bmp.GetWidth(), bmp.GetHeight()
            hasMask = bmp.GetMask() is not None
        else:
            # no bitmap -> size is zero
            bw = bh = 0

        label = self.GetLabel()
        dc.SetFont(self.GetFont())

        # size of text
        tw, th = dc.GetTextExtent(label)
        if self.GetToggle():
            dx = self.toggleShiftX
            dy = self.toggleShiftY

        contentWidth = bw + tw + self.marginImage

        if self.align == wx.ALIGN_LEFT:
            pos_x = self.padding + dx
        elif self.align == wx.ALIGN_CENTER:
            pos_x = (width - contentWidth - self.toggleShiftX) / 2 + dx
        else:
            assert False

        if pos_x < self.padding + dx:
            pos_x = self.padding + dx

        if bmp is not None:
            # draw bitmap if available
            dc.DrawBitmap(bmp, pos_x, (height - bh) / 2 + dy, hasMask)

        dc.DrawText(label, pos_x + bw + self.marginImage, (height-th)/2+dy)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
        panel = wx.Panel(self)

        # Build a bitmap button and a normal one
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))

        btn = ToggleButton(panel, -1, bmp, label=u'adsfasdf', pos=(10, 10))
        btn.SetSize((150, 75))

        btn2 = ToggleButton(panel, -1, bmp, label=u'adsfasdf', pos=(10, 110), align=wx.ALIGN_CENTER)
        btn2.SetSize((150, 75))

        btn3 = ToggleButton(panel, -1, bmp, label=u'adsfasdfadsf', pos=(10, 210), align=wx.ALIGN_CENTER)
        btn3.SetSize(btn3.GetMinSize())
        btn3.SetRoundRadius(0)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'ToggleButton Test')
    frame.Show()
    frame.SetSize((500, 600))
    app.MainLoop()

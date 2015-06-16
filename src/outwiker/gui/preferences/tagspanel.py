# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import TagsConfig


class TagsPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.config = TagsConfig (Application.config)

        self._createGui()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        self._createColorsGui (mainSizer)

        self.SetSizer (mainSizer)


    def _createColorsGui (self, mainsizer):
        self.colorFontNormalLabel = wx.StaticText (self, label = _(u'Tag color'))
        self.colorFontNormalPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorFontNormalHoverLabel = wx.StaticText (self, label = _(u'Hover tag color'))
        self.colorFontNormalHoverPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorFontSelectedLabel = wx.StaticText (self, label = _(u'Marked tag color'))
        self.colorFontSelectedPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorFontSelectedHoverLabel = wx.StaticText (self, label = _(u'Hover marked tag color'))
        self.colorFontSelectedHoverPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorBackSelectedLabel = wx.StaticText (self, label = _(u'Marked tag background'))
        self.colorBackSelectedPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        colorsSizer.Add(self.colorFontNormalLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontNormalPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        colorsSizer.Add(self.colorFontSelectedLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontSelectedPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        colorsSizer.Add(self.colorBackSelectedLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorBackSelectedPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        colorsSizer.Add(self.colorFontNormalHoverLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontNormalHoverPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        colorsSizer.Add(self.colorFontSelectedHoverLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontSelectedHoverPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        mainsizer.Add (colorsSizer, 0, wx.EXPAND | wx.ALL, border = 2)


    def LoadState(self):
        self.colorFontNormalPicker.SetColour (self.config.colorFontNormal.value)
        self.colorFontNormalHoverPicker.SetColour (self.config.colorFontNormalHover.value)

        self.colorFontSelectedPicker.SetColour (self.config.colorFontSelected.value)
        self.colorFontSelectedHoverPicker.SetColour (self.config.colorFontSelectedHover.value)

        self.colorBackSelectedPicker.SetColour (self.config.colorBackSelected.value)


    def Save (self):
        self.config.colorFontNormal.value = self.colorFontNormalPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self.config.colorFontNormalHover.value = self.colorFontNormalHoverPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

        self.config.colorFontSelected.value = self.colorFontSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self.config.colorFontSelectedHover.value = self.colorFontSelectedHoverPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

        self.config.colorBackSelected.value = self.colorBackSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

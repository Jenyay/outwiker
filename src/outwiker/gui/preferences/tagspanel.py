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
        self.colorFontNormalLabel = wx.StaticText (self, label = _(u'Normal tags color'))
        self.colorFontNormalPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorFontSelectedlLabel = wx.StaticText (self, label = _(u'Selected tags color'))
        self.colorFontSelectedPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        self.colorBackSelectedlLabel = wx.StaticText (self, label = _(u'Selected tags background'))
        self.colorBackSelectedPicker = wx.ColourPickerCtrl(self, style=wx.CLRP_SHOW_LABEL)

        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        colorsSizer.Add(self.colorFontNormalLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontNormalPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)
        colorsSizer.Add(self.colorFontSelectedlLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorFontSelectedPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)
        colorsSizer.Add(self.colorBackSelectedlLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        colorsSizer.Add(self.colorBackSelectedPicker, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

        mainsizer.Add (colorsSizer, 0, wx.EXPAND | wx.ALL, border = 2)


    def LoadState(self):
        self.colorFontNormalPicker.SetColour (self.config.colorFontNormal.value)
        self.colorFontSelectedPicker.SetColour (self.config.colorFontSelected.value)
        self.colorBackSelectedPicker.SetColour (self.config.colorBackSelected.value)


    def Save (self):
        self.config.colorFontNormal.value = self.colorFontNormalPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self.config.colorFontSelected.value = self.colorFontSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self.config.colorBackSelected.value = self.colorBackSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

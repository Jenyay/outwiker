# -*- coding: UTF-8 -*-

import wx

import configelements
from outwiker.core.application import Application
from outwiker.core.config import FontOption
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.gui.guiconfig import HtmlRenderConfig


class HtmlRenderPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.config = HtmlRenderConfig (Application.config)

        self._createGuiElements()
        self._do_layout()


    def _createGuiElements (self):
        # Font elements
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)

        # Html improver
        self.improverLabel = wx.StaticText(self, -1, _("Paragraphs separator"))
        self.improverComboBox = wx.ComboBox (self, -1, style = wx.CB_READONLY | wx.CB_DROPDOWN)

        # User's styles elements
        self.userStyleLabel = wx.StaticText(self, -1, _("Additional styles (CSS):"))
        self.userStyleTextBox = wx.TextCtrl(self,
                                            -1,
                                            "",
                                            style = wx.TE_PROCESS_ENTER | wx.TE_MULTILINE | wx.HSCROLL | wx.TE_LINEWRAP | wx.TE_WORDWRAP)


    def _do_layout(self):
        # Font
        fontSizer = wx.FlexGridSizer(cols=2)
        fontSizer.AddGrowableCol(1)
        fontSizer.Add(self.fontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        fontSizer.Add(self.fontPicker, 1, wx.EXPAND | wx.ALL, border=2)

        # HTML improver
        improverSizer = wx.FlexGridSizer (cols=2)
        improverSizer.AddGrowableCol(1)
        improverSizer.Add (self.improverLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        improverSizer.Add(self.improverComboBox, 1, wx.EXPAND | wx.ALL, border=2)

        # User's styles
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(3)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(fontSizer, 1, wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(improverSizer, 1, wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(self.userStyleLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        mainSizer.Add(self.userStyleTextBox, 0, wx.ALL | wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(mainSizer)


    def LoadState(self):
        # The font for HTML render
        fontOption = FontOption (self.config.fontName,
                                 self.config.fontSize,
                                 self.config.fontIsBold,
                                 self.config.fontIsItalic)

        self.fontEditor = configelements.FontElement (fontOption, self.fontPicker)

        self.userStyle = configelements.StringElement (self.config.userStyle, self.userStyleTextBox)

        self._fillHtmlImprovers (self.config)


    def Save (self):
        self.fontEditor.save()
        self.userStyle.save()

        selectedImprover = self.improverComboBox.GetSelection()
        self.config.HTMLImprover.value = self.improverComboBox.GetClientData (selectedImprover)


    def _fillHtmlImprovers (self, config):
        self.improverComboBox.Clear()

        factory = HtmlImproverFactory()
        for name in factory.names:
            self.improverComboBox.Append (factory.getDescription (name), name)

        selectedName = config.HTMLImprover.value

        self.improverComboBox.SetSelection (0)

        for n in range (self.improverComboBox.GetCount()):
            if self.improverComboBox.GetClientData (n) == selectedName:
                self.improverComboBox.SetSelection (n)
                break

        if len (factory.names) < 2:
            self.improverComboBox.Hide()
            self.improverLabel.Hide()

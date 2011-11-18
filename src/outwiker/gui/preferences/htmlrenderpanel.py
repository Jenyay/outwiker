#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

import configelements
from outwiker.core.application import Application
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.core.config import FontOption, StringOption


class HtmlRenderPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.__createGuiElements()

        self.__set_properties()
        self.__do_layout()

        self.config = HtmlRenderConfig (Application.config)

        self.LoadState()


    def __createGuiElements (self):
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)
        self.userStyleLabel = wx.StaticText(self, -1, _("Additional styles (CSS):"))
        self.userStyleTextBox = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.HSCROLL|wx.TE_LINEWRAP|wx.TE_WORDWRAP)


    def __set_properties(self):
        self.SetSize((415, 257))


    def __do_layout(self):
        fontSizer = wx.FlexGridSizer(1, 2, 0, 0)
        fontSizer.Add(self.fontLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.Add(self.fontPicker, 1, wx.EXPAND, 0)
        fontSizer.AddGrowableCol(1)

        mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
        mainSizer.Add(fontSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.userStyleLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.userStyleTextBox, 0, wx.ALL|wx.EXPAND, 2)
        mainSizer.AddGrowableRow(2)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)


    def LoadState(self):
        # Шрифт для HTML-рендера
        fontOption = FontOption (self.config.fontFaceNameOption, 
                self.config.fontSizeOption, 
                self.config.fontIsBold, 
                self.config.fontIsItalic)

        self.fontEditor = configelements.FontElement (fontOption, self.fontPicker)

        self.userStyle = configelements.StringElement (self.config.userStyleOption, self.userStyleTextBox)


    def Save (self):
        self.fontEditor.save()
        self.userStyle.save()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

import configelements
from outwiker.core.application import Application
from outwiker.gui.guiconfig import EditorConfig
from outwiker.core.config import FontOption


class EditorPanel(wx.Panel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50
        
        self.__config = EditorConfig (Application.config)
        self.__createGuiElements (self.__config)

        self.__set_properties()
        self.__do_layout()

        self.LoadState()


    def __createGuiElements (self, config):
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)
        self.lineNumbersCheckBox = wx.CheckBox(self, -1, _("Show line numbers"))
        self.tabWidthLabel = wx.StaticText(self, -1, _("Tab width"))

        self.tabWidthSpin = wx.SpinCtrl(self, 
                -1, 
                str (config.TAB_WIDTH_DEFAULT), 
                min=self.MIN_TAB_WIDTH, 
                max=self.MAX_TAB_WIDTH, 
                style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL)


    def __set_properties(self):
        self.DEFAULT_WIDTH = 400
        self.DEFAULT_HEIGHT = 250

        self.SetSize((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))


    def __do_layout(self):
        fontSizer = wx.FlexGridSizer(1, 2, 0, 0)
        fontSizer.Add(self.fontLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.Add(self.fontPicker, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.AddGrowableRow(0)
        fontSizer.AddGrowableCol(1)

        tabWidthSizer = wx.FlexGridSizer(1, 2, 0, 0)
        tabWidthSizer.Add(self.tabWidthLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        tabWidthSizer.Add(self.tabWidthSpin, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        tabWidthSizer.AddGrowableCol(1)

        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.Add(fontSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.lineNumbersCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(tabWidthSizer, 1, wx.EXPAND, 0)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)


    def LoadState(self):
        # Показывать ли номера строк?
        self.lineNumbers = configelements.BooleanElement (self.__config.lineNumbers, self.lineNumbersCheckBox)

        # Шрифт для редактора
        fontOption = FontOption (self.__config.fontName, 
                self.__config.fontSize, 
                self.__config.fontIsBold, 
                self.__config.fontIsItalic)

        self.fontEditor = configelements.FontElement (fontOption, self.fontPicker)

        # Размер табуляции
        self.tabWidth = configelements.IntegerElement (self.__config.tabWidth, 
                self.tabWidthSpin, 
                self.MIN_TAB_WIDTH, 
                self.MAX_TAB_WIDTH)
    

    def Save (self):
        self.lineNumbers.save()
        self.fontEditor.save()
        self.tabWidth.save()


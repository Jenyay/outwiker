#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.editorstyleslist import EditorStylesList


class HtmlEditorPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        # self.config = HtmlRenderConfig (Application.config)

        self.__createGui()
        self.__layout()

        self.LoadState()


    def __createGui (self):
        self._stylesList = EditorStylesList (self)


    def __layout(self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._stylesList, flag = wx.ALL | wx.EXPAND, border = 2)

        self.SetSizer (mainSizer)
        self.Layout()


    def LoadState(self):
        pass
        # # Шрифт для HTML-рендера
        # fontOption = FontOption (self.config.fontName, 
        #         self.config.fontSize, 
        #         self.config.fontIsBold, 
        #         self.config.fontIsItalic)

        # self.fontEditor = configelements.FontElement (fontOption, self.fontPicker)

        # self.userStyle = configelements.StringElement (self.config.userStyle, self.userStyleTextBox)


    def Save (self):
        pass
        # self.fontEditor.save()
        # self.userStyle.save()

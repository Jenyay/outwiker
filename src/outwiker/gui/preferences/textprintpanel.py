# -*- coding: UTF-8 -*-

import wx

from . import configelements
from outwiker.core.config import FontOption
from outwiker.gui.guiconfig import TextPrintConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class TextPrintPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super(type(self), self).__init__(parent)

        self.__createGuiElements()
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onPageOptions, self.pageOptionsBtn)

        self.config = TextPrintConfig(application.config)
        self.LoadState()
        self.SetupScrolling()

    def __createGuiElements(self):
        self.sharedTextLabel = wx.StaticText(self, -1,
                                             _("This options for text printing only"),
                                             style=wx.ALIGN_CENTRE)
        self.fontLabel = wx.StaticText(self, -1, _("Font"))
        self.fontPicker = wx.FontPickerCtrl(self, -1)
        self.pageOptionsBtn = wx.Button(self, -1, _("Page Options..."))

    def __set_properties(self):
        DEFAULT_WIDTH = 400
        DEFAULT_HEIGHT = 300
        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))

        FONT_LABEL_WIDTH = 200
        self.fontLabel.SetMinSize((FONT_LABEL_WIDTH, -1))

    def __do_layout(self):
        fontSizer = wx.FlexGridSizer(1, 2, 0, 0)
        fontSizer.Add(self.fontLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        fontSizer.Add(self.fontPicker, 1, wx.EXPAND, 0)
        fontSizer.AddGrowableCol(1)

        mainSizer = wx.FlexGridSizer(3, 1, 0, 0)
        mainSizer.Add(self.sharedTextLabel, 0, wx.ALL, 2)
        mainSizer.Add(fontSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.pageOptionsBtn, 0, wx.ALL, 2)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)

    def onPageOptions(self, event):
        pd = wx.PrintData()
        psdd = wx.PageSetupDialogData(pd)

        psdd.SetMarginTopLeft(wx.Point(self.config.marginLeft.value, self.config.marginTop.value))
        psdd.SetMarginBottomRight(wx.Point(self.config.marginRight.value, self.config.marginBottom.value))
        psdd.SetPaperId(self.config.paperId.value)

        dlg = wx.PageSetupDialog(self, psdd)

        if dlg.ShowModal() == wx.ID_OK:
            psdd_new = dlg.GetPageSetupData()

            marginLeftTop = psdd_new.GetMarginTopLeft()
            marginRightBottom = psdd_new.GetMarginBottomRight()

            self.config.marginLeft.value = marginLeftTop[0]
            self.config.marginTop.value = marginLeftTop[1]

            self.config.marginRight.value = marginRightBottom[0]
            self.config.marginBottom.value = marginRightBottom[1]

            self.config.paperId.value = psdd_new.GetPaperId()

    def LoadState(self):
        # Обычный шрифт
        fontOption = FontOption(self.config.fontName,
                                self.config.fontSize,
                                self.config.fontIsBold,
                                self.config.fontIsItalic)

        self.font = configelements.FontElement(fontOption, self.fontPicker)

    def Save(self):
        self.font.save()

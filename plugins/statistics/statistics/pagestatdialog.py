#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class PageStatDialog (wx.Dialog):
    """Диалог для показа статистики одной страницы"""
    def __init__(self, parent, pageStat):
        """
        pageStat - экземпляр класса PageStat
        """
        super(PageStatDialog, self).__init__(parent)

        global _
        _ = get_()

        self._createGui ()
        self.Fit()
        self.Center (wx.CENTRE_ON_SCREEN)

        self._updateStatistics (pageStat)


    def _updateStatistics (self, pageStat):
        try:
            self.wordsText.SetValue (str (pageStat.words) )
        except TypeError:
            pass


        try:
            self.linesText.SetValue (str (pageStat.lines) )
        except TypeError:
            pass


        try:
            self.symbolsText.SetValue (str (pageStat.symbols) )
        except TypeError:
            pass


        try:
            self.symbolsWithoutSpacesText.SetValue (str (pageStat.symbolsNotWhiteSpaces) )
        except TypeError:
            pass


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)


        # Количество слов
        wordsLabel = wx.StaticText (self, label=_(u"Word count"))
        self.wordsText = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.wordsText.SetMinSize ((100, -1))

        mainSizer.Add (wordsLabel, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        mainSizer.Add (self.wordsText, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)


        # Количество строк
        linesLabel = wx.StaticText (self, label=_(u"Line count"))
        self.linesText = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.linesText.SetMinSize ((100, -1))

        mainSizer.Add (linesLabel, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        mainSizer.Add (self.linesText, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)


        # Количество символов
        symbolsLabel = wx.StaticText (self, label=_(u"Character count"))
        self.symbolsText = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.symbolsText.SetMinSize ((100, -1))

        mainSizer.Add (symbolsLabel, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        mainSizer.Add (self.symbolsText, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)


        # Количество символов без пробелов
        symbolsWithoutSpacesLabel = wx.StaticText (self, label=_(u"Character count without spaces"))
        self.symbolsWithoutSpacesText = wx.TextCtrl (self, style=wx.TE_READONLY)
        self.symbolsWithoutSpacesText.SetMinSize ((100, -1))

        mainSizer.Add (symbolsWithoutSpacesLabel, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        mainSizer.Add (self.symbolsWithoutSpacesText, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)


        mainSizer.AddStretchSpacer()
        okBtn = wx.Button (self, wx.ID_OK)
        okBtn.SetDefault()

        mainSizer.Add (okBtn, 
                1,
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        self.SetSizer (mainSizer)
        self.Layout()

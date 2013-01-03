#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class InsertDialog (wx.Dialog):
    """
    Диалог для вставки команды (:source:)
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertDialog, self).__init__ (parent, 
                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                title=_(u"Source code"))

        self.__createGui()
        self.languageComboBox.SetFocus()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)


    @property
    def language (self):
        return self.languageComboBox.GetValue()


    @property
    def tabWidth (self):
        return self.tabWidthSpin.GetValue()


    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (0, 2)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(2)

        self.__createLanguageGui (mainSizer)
        self.__createTabWidthGui (mainSizer)
        self.__createOkCancelButtons (mainSizer)

        self.SetSizer(mainSizer)
        self.Layout()


    def __createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (
                okCancel,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                border=2
                )


    def __createLanguageGui (self, mainSizer):
        """
        Создать интерфейс, связанный с языком программирования по умолчанию
        """
        languageLabel = wx.StaticText(self, -1, _(u"Programming Language"))
        self.languageComboBox = wx.ComboBox (self, 
                style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)

        self.languageComboBox.SetMinSize (wx.Size (150, -1))

        mainSizer.Add (
                languageLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        mainSizer.Add (
                self.languageComboBox, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
                border=2
                )


    def __createTabWidthGui (self, mainSizer):
        """
        Создать интерфейс, связанный с размером табуляции
        """
        tabWidthLabel = wx.StaticText(self, -1, _(u"Tab Width"))
        self.tabWidthSpin = wx.SpinCtrl (
                self, 
                style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL
                )
        self.tabWidthSpin.SetMinSize (wx.Size (150, -1))


        mainSizer.Add (
                tabWidthLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        mainSizer.Add (
                self.tabWidthSpin, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
                border=2
                )

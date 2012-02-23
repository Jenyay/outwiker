#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

class LogDialog (wx.Dialog):
    def __init__ (self, parent, logList):
        from .i18n import _
        global _

        wx.Dialog.__init__ (self, 
                parent, 
                title=_(u"Errors List"), 
                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER )

        logMinWidth = 550
        logMinHeight = 350
        self.__logText = wx.TextCtrl (self, 
                style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.__logText.SetMinSize ((logMinWidth, logMinHeight))

        log = u"\n\n".join (logList)
        self.__logText.SetValue (log)

        self.__buttonsSizer = self.CreateButtonSizer (wx.OK)

        self.__layout()
        self.__centerWindow()


    def __centerWindow (self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self.GetSize()

        parentWidth, parentHeight = self.GetParent().GetSize()
        parentX, parentY = self.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self.SetPosition ((posX, posY))


    def __layout (self):
        mainSizer = wx.FlexGridSizer (rows=2, cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self.__logText, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add (self.__buttonsSizer, flag=wx.ALL | wx.ALIGN_CENTER, border=2)

        self.SetSizer (mainSizer)
        self.Fit()
        self.Layout()

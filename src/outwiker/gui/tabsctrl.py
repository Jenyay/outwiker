#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.aui


class TabsCtrl (wx.Panel):
    def __init__ (self, parent):
        super (TabsCtrl, self).__init__ (parent)

        self._tabs = wx.aui.AuiNotebook (self)
        self.__layout()


    def __layout (self):
        self.updateSize()
        mainSizer = wx.FlexGridSizer (1, 0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._tabs, 0, wx.EXPAND)
        self.SetSizer (mainSizer)
        self.Layout()
        self.updateSize()


    def updateSize (self):
        self.SetMaxSize ((-1, self._tabs.GetTabCtrlHeight()))
        self.SetMinSize ((-1, self._tabs.GetTabCtrlHeight()))


    def addPage (self, title, page):
        blankWindow = wx.Window (self, size=(1,1))
        blankWindow.page = page
        self._tabs.AddPage (blankWindow, title)
        self.updateSize()
        return blankWindow


    def clear (self):
        count = self._tabs.GetPageCount()
        for _ in range (count):
            self._tabs.DeletePage (0)


    def renameCurrentTab (self, title):
        page_index = self._tabs.GetSelection()
        if page_index >= 0:
            self._tabs.SetPageText (page_index, title)


    def getPage (self, index):
        return self._tabs.GetPage (index).page


    def setCurrentPage (self, page):
        page_index = self._tabs.GetSelection()
        if page_index >= 0:
            self._tabs.GetPage (page_index).page = page

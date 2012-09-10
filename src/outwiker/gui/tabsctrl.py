#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.agw.flatnotebook as fnb


class TabsCtrl (wx.Panel):
    def __init__ (self, parent):
        super (TabsCtrl, self).__init__ (parent)

        self._tabs = fnb.FlatNotebook (self, agwStyle = (fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS | 
            fnb.FNB_X_ON_TAB))

        self.__layout()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (1, 0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._tabs, 0, wx.EXPAND)
        self.SetSizer (mainSizer)
        self.Layout()


    def addPage (self, title, page):
        blankWindow = wx.Window (self, size=(1,1))
        blankWindow.page = page
        self._tabs.AddPage (blankWindow, title)
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


    def getSelection (self):
        return self._tabs.GetSelection()


    def getPages (self):
        return [self._tabs.GetPage (index).page for index in range (self._tabs.GetPageCount())]


    def getPageCount (self):
        return self._tabs.GetPageCount()


    def setSelection (self, index):
        return self._tabs.SetSelection (index)


    def deletePage (self, index):
        return self._tabs.DeletePage (index)

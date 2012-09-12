#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.agw.flatnotebook as fnb


class TabsCtrl (wx.Panel):
    def __init__ (self, parent):
        super (TabsCtrl, self).__init__ (parent)

        self._tabs = fnb.FlatNotebook (self, agwStyle = (fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS | 
            fnb.FNB_X_ON_TAB | 
            fnb.FNB_SMART_TABS))

        self.__layout()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (1, 0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._tabs, 0, wx.EXPAND)
        self.SetSizer (mainSizer)
        self.Layout()


    def AddPage (self, title, page):
        blankWindow = wx.Window (self, size=(1,1))
        blankWindow.page = page
        self._tabs.AddPage (blankWindow, title)


    def InsertPage (self, index, title, page, select):
        blankWindow = wx.Window (self, size=(1,1))
        blankWindow.page = page
        self._tabs.InsertPage (index, blankWindow, title, select)


    def Clear (self):
        self._tabs.DeleteAllPages()


    def GetPageText (self, index):
        return self._tabs.GetPageText (index)


    def RenameCurrentTab (self, title):
        page_index = self.GetSelection()
        if page_index >= 0:
            self.RenameTab (page_index, title)


    def RenameTab (self, index, title):
        self._tabs.SetPageText (index, title)


    def GetPage (self, index):
        return self._tabs.GetPage (index).page


    def SetCurrentPage (self, page):
        page_index = self.GetSelection()
        if page_index >= 0:
            self._tabs.GetPage (page_index).page = page


    def GetSelection (self):
        return self._tabs.GetSelection()


    def GetPages (self):
        return [self.GetPage (index) for index in range (self.GetPageCount())]


    def GetPageCount (self):
        return self._tabs.GetPageCount()


    def SetSelection (self, index):
        return self._tabs.SetSelection (index)


    def DeletePage (self, index):
        return self._tabs.DeletePage (index)

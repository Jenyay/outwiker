# -*- coding: UTF-8 -*-

import wx
import wx.lib.agw.flatnotebook as fnb

from outwiker.core.application import Application
from outwiker.core.history import History
from outwiker.actions.history import HistoryBackAction, HistoryForwardAction


class TabsCtrl (wx.Panel):
    def __init__ (self, parent):
        super (TabsCtrl, self).__init__ (parent)

        self._tabs = fnb.FlatNotebook (self, agwStyle = (fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS | 
            fnb.FNB_X_ON_TAB |
            fnb.FNB_DROPDOWN_TABS_LIST))

        self.__layout()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (1, 0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._tabs, 0, wx.EXPAND)
        self.SetSizer (mainSizer)
        self.Layout()


    def _updateHistoryButtons (self):
        """
        Активировать или дезактивировать кнопки Вперед / Назад
        """
        history = self._getCurrentHistory()
        if history == None:
            Application.actionController.enableTools (HistoryBackAction.stringId, False)
            Application.actionController.enableTools (HistoryForwardAction.stringId, False)
        else:
            Application.actionController.enableTools (HistoryBackAction.stringId, 
                    history.backLength != 0)
            Application.actionController.enableTools (HistoryForwardAction.stringId, 
                    history.forwardLength != 0)



    def AddPage (self, title, page):
        blankWindow = TabWindow (self, page)
        self._tabs.AddPage (blankWindow, title)


    def InsertPage (self, index, title, page, select):
        blankWindow = TabWindow (self, page)
        self._tabs.InsertPage (index, blankWindow, title, select)
        self._updateHistoryButtons()


    def Clear (self):
        self._tabs.DeleteAllPages()
        self._updateHistoryButtons()


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

        self._updateHistoryButtons()


    def _getCurrentHistory (self):
        """
        Возвращает класс истории для текущей вкладки
        """
        page_index = self.GetSelection()

        if page_index >= 0:
            return self._tabs.GetPage (page_index).history


    def GetSelection (self):
        return self._tabs.GetSelection()


    def GetPages (self):
        return [self.GetPage (index) for index in range (self.GetPageCount())]


    def GetPageCount (self):
        return self._tabs.GetPageCount()


    def SetSelection (self, index):
        result = self._tabs.SetSelection (index)
        self._updateHistoryButtons()
        return result


    def DeletePage (self, index):
        result = self._tabs.DeletePage (index)
        self._updateHistoryButtons()
        return result


    def DeletePage (self, index):
        self._tabs.DeletePage (index)
        self._updateHistoryButtons()


    def NextPage (self):
        self._tabs.AdvanceSelection(True)
        self._updateHistoryButtons()


    def PreviousPage (self):
        self._tabs.AdvanceSelection (False)
        self._updateHistoryButtons()


    def HistoryBack (self):
        page = self._getCurrentHistory().back()
        Application.selectedPage = page
        self._updateHistoryButtons()


    def HistoryForward (self):
        page = self._getCurrentHistory().forward()
        Application.selectedPage = page
        self._updateHistoryButtons()


class TabWindow (wx.Window):
    """
    Класс окна, хранимого внутри владки с дополнительной информацией (текущая страница, история)
    """
    def __init__ (self, parent, page):
        super (TabWindow, self).__init__ (parent, size=(1, 1) )
        self._history = History()
        self._history.goto (page)

    
    @property
    def page (self):
        return self._history.currentPage


    @page.setter
    def page (self, page):
        self._history.goto (page)


    @property
    def history (self):
        return self._history

# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod

import wx

from outwiker.gui.controls.searchreplacepanel import SearchReplacePanel


class BaseHtmlSearchPanelController(metaclass=ABCMeta):
    def __init__(self, searchPanel: SearchReplacePanel, htmlRender):
        """
        searchPanel - панель со строкой поиска
        htmlRender - HTML render control
        """
        # Панель со строкой поиска
        self._panel = searchPanel
        self._htmlRender = htmlRender

        self.setSearchPhrase('')
        self._panel.setReplaceGuiVisible(False)
        self._panel.setPrevButtonVisible(False)
        self._panel.setResultLabelVisible(False)
        self.hidePanel()
        self._bindGui(self._panel)

    @abstractclassmethod
    def startSearch(self):
        pass

    @abstractclassmethod
    def nextSearch(self):
        pass

    @abstractclassmethod
    def enterSearchPhrase(self):
        pass

    def prevSearch(self):
        pass

    def _bindGui(self, panel):
        panel.Bind(wx.EVT_CLOSE, self._onClose)
        panel.Bind(wx.EVT_TEXT_ENTER, self._onEnterPress, panel.getSearchTextCtrl())
        panel.Bind(wx.EVT_TEXT, self._onSearchTextChange, panel.getSearchTextCtrl())
        panel.Bind(wx.EVT_BUTTON, self._onNextSearch, panel.getNextSearchBtn())
        panel.Bind(wx.EVT_BUTTON, self._onCloseClick, panel.getCloseBtn())

    def show(self):
        if not self._panel.IsShown():
            self._panel.Show()
            self._panel.Fit()
            self._panel.GetParent().Layout()

    def setSearchPhrase(self, phrase):
        """
        В панели поиска установить искомую фразу.
        При этом сразу начинается поиск
        """
        self._panel.getSearchTextCtrl().SetValue(phrase)

    def getSearchPhrase(self):
        """
        Возвращает искомую фразу из панели
        """
        return self._panel.getSearchTextCtrl().GetValue()

    def getPanel(self):
        return self._panel

    @property
    def htmlRender(self):
        return self._htmlRender

    def _onEnterPress(self, _event):
        self.nextSearch()

    def _onNextSearch(self, _event):
        self.nextSearch()

    def _onSearchTextChange(self, _event):
        self.enterSearchPhrase()

    def _onCloseClick(self, _event):
        self._panel.Close()

    def _onClose(self, _event):
        self.hidePanel()

    def hidePanel(self):
        self.htmlRender.SetFocus()
        self._panel.Hide()
        self._panel.GetParent().Layout()

    def switchToSearchMode(self):
        pass

# -*- coding: utf-8 -*-

import wx

from outwiker.gui.controls.searchreplacepanel import SearchReplacePanel


class HtmlSearchPanelController:
    def __init__(self, searchPanel: SearchReplacePanel, htmlRender):
        """
        searchPanel - панель со строкой поиска
        htmlRender - HTML render control
        """
        # Панель со строкой поиска
        self.panel = searchPanel
        self.htmlRender = htmlRender

        self.setSearchPhrase('')
        self.panel.setReplaceGuiVisible(False)
        self.panel.setPrevButtonVisible(False)
        self.panel.setResultLabelVisible(False)
        self.hidePanel()
        self._bindGui(self.panel)

    def _bindGui(self, panel):
        panel.Bind(wx.EVT_CLOSE, self._onClose)
        panel.Bind(wx.EVT_TEXT_ENTER, self._onEnterPress, panel.getSearchTextCtrl())
        panel.Bind(wx.EVT_TEXT, self._onSearchTextChange, panel.getSearchTextCtrl())
        panel.Bind(wx.EVT_BUTTON, self._onNextSearch, panel.getNextSearchBtn())
        panel.Bind(wx.EVT_BUTTON, self._onCloseClick, panel.getCloseBtn())

    def _onEnterPress(self, _event):
        self.nextSearch()

    def _onNextSearch(self, _event):
        self.nextSearch()

    def _onSearchTextChange(self, _event):
        self.enterSearchPhrase()

    def _onCloseClick(self, _event):
        self.panel.Close()

    def _onClose(self, _event):
        self.hidePanel()

    def switchToSearchMode(self):
        pass

    def hidePanel(self):
        self.htmlRender.SetFocus()
        self.panel.Hide()
        self.panel.GetParent().Layout()

    def nextSearch(self):
        """
        Искать следующее вхождение фразы
        """
        self._search(False)

    def startSearch(self):
        """
        Начать поиск
        """
        self.setSearchPhrase(self.getSearchPhrase())
        self.htmlRender.Find('')
        self.panel.getSearchTextCtrl().SetSelection(-1, -1)
        self.panel.getSearchTextCtrl().SetFocus()
        self._search(True)

    def enterSearchPhrase(self):
        self._search(True)

    def show(self):
        if not self.panel.IsShown():
            self.panel.Show()
            self.panel.Fit()
            self.panel.GetParent().Layout()

    def setSearchPhrase(self, phrase):
        """
        В панели поиска установить искомую фразу.
        При этом сразу начинается поиск
        """
        self.panel.getSearchTextCtrl().SetValue(phrase)

    def getSearchPhrase(self):
        """
        Возвращает искомую фразу из панели
        """
        return self.panel.getSearchTextCtrl().GetValue()

    def _search(self, newSearch: bool):
        """
        Поиск фразы в нужном направлении (вперед / назад)
        """
        phrase = self.getSearchPhrase()

        if len(phrase) == 0:
            return

        result = self.htmlRender.Find(phrase)
        if newSearch and result:
            self.htmlRender.Find(phrase)

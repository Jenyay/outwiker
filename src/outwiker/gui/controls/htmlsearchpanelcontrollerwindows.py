# -*- coding: utf-8 -*-

from .basehtmlsearchpanelcontroller import BaseHtmlSearchPanelController


class HtmlSearchPanelControllerWindows(BaseHtmlSearchPanelController):
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
        self.getPanel().getSearchTextCtrl().SetSelection(-1, -1)
        self.getPanel().getSearchTextCtrl().SetFocus()
        self._search(True)

    def enterSearchPhrase(self):
        self._search(True)

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

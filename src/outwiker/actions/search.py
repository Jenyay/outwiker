# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class BaseSearchAction (BaseAction):
    """
    Базовый класс для actions поиска по странице
    """

    def __init__(self, application):
        self._application = application

    def _getPageView(self):
        return self._application.mainWindow.pagePanel.panel.pageView

    def _getSearchPanel(self):
        return self._getPageView().GetSearchPanel()


class SearchAction (BaseSearchAction):
    """
    Начать поиск на странице
    """
    stringId = u"Search"

    @property
    def title(self):
        return _(u"Search")

    @property
    def description(self):
        return _(u"Find on page")

    def run(self, params):
        searchPanel = self._getSearchPanel()

        if searchPanel is not None:
            searchPanel.switchToSearchMode()
            searchPanel.show()
            searchPanel.startSearch()


class SearchNextAction (BaseSearchAction):
    """
    Найти следующее вхождение на странице
    """
    stringId = u"SearchNext"

    @property
    def title(self):
        return _(u"Find next")

    @property
    def description(self):
        return _(u"Find next on page")

    def run(self, params):
        searchPanel = self._getSearchPanel()

        if searchPanel is not None:
            searchPanel.show()
            searchPanel.nextSearch()


class SearchPrevAction (BaseSearchAction):
    """
    Найти предыдущее вхождение на странице
    """
    stringId = u"SearchPrev"

    @property
    def title(self):
        return _(u"Find previous")

    @property
    def description(self):
        return _(u"Find previous on page")

    def run(self, params):
        searchPanel = self._getSearchPanel()

        if searchPanel is not None:
            searchPanel.show()
            searchPanel.prevSearch()


class SearchAndReplaceAction (BaseSearchAction):
    """
    Начать поиск и замену на странице
    """
    stringId = u"SearchReplace"

    @property
    def title(self):
        return _(u"Search and Replace")

    @property
    def description(self):
        return _(u"Begin search and replace on page")

    def run(self, params):
        searchPanel = self._getSearchPanel()

        if searchPanel is not None:
            searchPanel.switchToReplaceMode()
            searchPanel.show()
            searchPanel.startSearch()

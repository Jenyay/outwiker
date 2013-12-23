#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction

class BaseSearchAction (BaseAction):
    """
    Базовый класс для actions поиска по странице
    """
    def __init__ (self, application):
        self._application = application


    def _showSearchPanel (self, searchPanel):
        if not searchPanel.IsShown():
            searchPanel.Show()
            searchPanel.GetParent().Layout()


    def _getPageView (self):
        return self._application.mainWindow.pagePanel.panel.pageView



class SearchAction (BaseSearchAction):
    """
    Начать поиск на странице
    """
    stringId = u"Search"

    @property
    def title (self):
        return _(u"Search")


    @property
    def description (self):
        return _(u"Find on page")


    def run (self, params):
        searchPanel = self._getPageView().GetSearchPanel()

        if searchPanel != None:
            self._showSearchPanel (searchPanel)
            searchPanel.startSearch()


class SearchNextAction (BaseSearchAction):
    """
    Найти следующее вхождение на странице
    """
    stringId = u"SearchNext"

    @property
    def title (self):
        return _(u"Find next")


    @property
    def description (self):
        return _(u"Find next on page")


    def run (self, params):
        searchPanel = self._getPageView().GetSearchPanel()

        if searchPanel != None:
            self._showSearchPanel (searchPanel)
            searchPanel.nextSearch()


class SearchPrevAction (BaseSearchAction):
    """
    Найти предыдущее вхождение на странице
    """
    stringId = u"SearchPrev"

    @property
    def title (self):
        return _(u"Find previous")


    @property
    def description (self):
        return _(u"Find previous on page")


    def run (self, params):
        searchPanel = self._getPageView().GetSearchPanel()

        if searchPanel != None:
            self._showSearchPanel (searchPanel)
            searchPanel.prevSearch()

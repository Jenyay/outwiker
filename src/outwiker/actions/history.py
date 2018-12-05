# -*- coding: utf-8 -*-
"""
Действия, связанные с кнопками вперед / назад
"""

from outwiker.gui.baseaction import BaseAction


class HistoryBackAction (BaseAction):
    """
    Назад
    """
    stringId = u"HistoryBack"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Back")

    @property
    def description(self):
        return _(u"Open previous page")

    def run(self, params):
        self._application.mainWindow.tabsController.historyBack()


class HistoryForwardAction (BaseAction):
    """
    Вперед
    """
    stringId = u"HistoryForward"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Forward")

    @property
    def description(self):
        return _(u"Open next page")

    def run(self, params):
        self._application.mainWindow.tabsController.historyForward()

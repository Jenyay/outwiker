# -*- coding: utf-8 -*-
"""
Действия, связанные с кнопками вперед / назад
"""

from outwiker.gui.baseaction import BaseAction


class HistoryBackAction(BaseAction):
    """
    Назад
    """
    stringId = "HistoryBack"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Back")

    @property
    def description(self):
        return _("Open previous page")

    def run(self, params):
        self._application.mainWindow.tabsController.historyBack()


class HistoryForwardAction(BaseAction):
    """
    Вперед
    """
    stringId = "HistoryForward"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Forward")

    @property
    def description(self):
        return _("Open next page")

    def run(self, params):
        self._application.mainWindow.tabsController.historyForward()

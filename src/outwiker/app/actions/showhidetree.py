# -*- coding: utf-8 -*-

from outwiker.api.gui.mainwindow import showHideNotesTreePanel
from outwiker.gui.baseaction import BaseAction


class ShowHideTreeAction(BaseAction):
    """
    Показать / скрыть панель с деревом заметок
    """
    stringId = "ShowHideTree"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Notes Tree")

    @property
    def description(self):
        return _("Show / hide a notes tree panel")

    def run(self, params):
        showHideNotesTreePanel(self._application, params)

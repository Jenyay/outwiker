# -*- coding: utf-8 -*-

from outwiker.app.gui.mainwindowtools import showHideNotesTreePanel
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
        return _("Note tree")

    @property
    def description(self):
        return _("Toggle the note tree panel")

    def run(self, params):
        showHideNotesTreePanel(self._application.mainWindow, params)

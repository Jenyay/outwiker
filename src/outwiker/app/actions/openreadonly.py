# -*- coding: utf-8 -*-

from outwiker.app.services.tree import openWikiWithDialog
from outwiker.gui.baseaction import BaseAction


class OpenReadOnlyAction(BaseAction):
    """
    Открытие дерева заметок
    """
    stringId = "OpenTreeReadOnly"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Open read-only…")

    @property
    def description(self):
        return _("Opens the note tree in read-only mode")

    def run(self, params):
        openWikiWithDialog(self._application.mainWindow, self._application, True)

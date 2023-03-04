# -*- coding: utf-8 -*-

from outwiker.api.services.tree import openWikiWithDialog
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
        return _("Open Read-only…")

    @property
    def description(self):
        return _("Open tree notes read only")

    def run(self, params):
        openWikiWithDialog(self._application.mainWindow, True)

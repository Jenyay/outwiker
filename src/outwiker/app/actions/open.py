# -*- coding: utf-8 -*-

from outwiker.app.services.tree import openWikiWithDialog
from outwiker.gui.baseaction import BaseAction


class OpenAction (BaseAction):
    """
    Открытие дерева заметок
    """
    stringId = "OpenTree"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Open…")

    @property
    def description(self):
        return _("Open tree notes")

    def run(self, params):
        openWikiWithDialog(self._application.mainWindow, False)

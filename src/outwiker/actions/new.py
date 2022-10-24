# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import createNewWiki


class NewAction(BaseAction):
    """
    Создание нового дерева заметок
    """
    stringId = "NewTree"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("New…")

    @property
    def description(self):
        return _("Create a new tree notes")

    def run(self, params):
        createNewWiki(self._application.mainWindow)

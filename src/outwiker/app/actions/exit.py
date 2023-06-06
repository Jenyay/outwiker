# -*- coding: utf-8 -*-

from outwiker.app.services.application import exit
from outwiker.gui.baseaction import BaseAction


class ExitAction(BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = "Exit"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Exit…")

    @property
    def description(self):
        return _("Close OutWiker")

    def run(self, params):
        exit(self._application)

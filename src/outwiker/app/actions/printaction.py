# -*- coding: utf-8 -*-

from outwiker.api.services.application import printCurrentPage
from outwiker.gui.baseaction import BaseAction


class PrintAction(BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = "Print"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Print")

    @property
    def description(self):
        return _("Print current page")

    def run(self, params):
        printCurrentPage(self._application)

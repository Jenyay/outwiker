# -*- coding: utf-8 -*-

from outwiker.api.core.tree import closeWiki
from outwiker.gui.baseaction import BaseAction


class CloseAction(BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = "CloseWiki"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Close")

    @property
    def description(self):
        return _("Close a tree notes")

    def run(self, params):
        closeWiki(self._application)

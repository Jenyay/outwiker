# -*- coding: utf-8 -*-

from outwiker.api.services.tree import removePage
from outwiker.gui.baseaction import BaseAction


class RemovePageAction(BaseAction):
    """
    Удалить текущую страницу
    """
    stringId = "RemovePage"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Remove Page…")

    @property
    def description(self):
        return _("Remove current page and all children")

    def run(self, params):
        if self._application.selectedPage is not None:
            removePage(self._application.wikiroot.selectedPage)

# -*- coding: utf-8 -*-

from outwiker.api.core.tree import testreadonly
from outwiker.api.services.messages import showError
from outwiker.gui.baseaction import BaseAction


class SortChildAlphabeticalAction(BaseAction):
    """
    Отсортировать дочерние страницы по алфавиту
    """
    stringId = "SortChildAlphabetically"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Sort Children Pages Alphabetically")

    @property
    def description(self):
        return _("Sort children pages alphabetically")

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.sortChildrenAlphabetical()
        else:
            self._application.wikiroot.sortChildrenAlphabetical()

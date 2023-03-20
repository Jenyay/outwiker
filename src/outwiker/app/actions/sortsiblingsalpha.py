# -*- coding: utf-8 -*-

from outwiker.app.services.messages import showError
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction


class SortSiblingsAlphabeticalAction (BaseAction):
    """
    Отсортировать страницы того же уровня по алфавиту
    """
    stringId = "SortSiblingsAlphabetically"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Sort Siblings Pages Alphabetically")

    @property
    def description(self):
        return _("Sort siblings pages alphabetically")

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.parent.sortChildrenAlphabetical()

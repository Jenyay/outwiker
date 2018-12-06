# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, showError


class SortChildAlphabeticalAction (BaseAction):
    """
    Отсортировать дочерние страницы по алфавиту
    """
    stringId = u"SortChildAlphabetically"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Sort Children Pages Alphabetically")

    @property
    def description(self):
        return _(u"Sort children pages alphabetically")

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _(u"Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.sortChildrenAlphabetical()
        else:
            self._application.wikiroot.sortChildrenAlphabetical()

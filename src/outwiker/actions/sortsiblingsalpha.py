# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, showError


class SortSiblingsAlphabeticalAction (BaseAction):
    """
    Отсортировать страницы того же уровня по алфавиту
    """
    stringId = u"SortSiblingsAlphabetically"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Sort Siblings Pages Alphabetically")

    @property
    def description(self):
        return _(u"Sort siblings pages alphabetically")

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _(u"Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.parent.sortChildrenAlphabetical()

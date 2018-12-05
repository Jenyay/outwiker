# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, MessageBox


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
            MessageBox(_(u"Wiki is not open"),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.parent.sortChildrenAlphabetical()

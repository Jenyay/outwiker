# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import openWikiWithDialog


class OpenReadOnlyAction (BaseAction):
    """
    Открытие дерева заметок
    """
    stringId = u"OpenTreeReadOnly"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Open Read-only…")


    @property
    def description (self):
        return _(u"Open tree notes read only")


    def run (self, params):
        openWikiWithDialog (self._application.mainWindow, True)

# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class SaveSessionAction (BaseAction):
    """
    Описание действия
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Sessions_SaveSession"


    @property
    def title (self):
        return _(u"Save session...")


    @property
    def description (self):
        return _(u"Save currently opened tabs")


    def run (self, params):
        print "Run!"

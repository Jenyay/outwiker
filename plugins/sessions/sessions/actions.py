# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class SaveSessionAction (BaseAction):
    """
    Действие для сохранения сессии
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
        print "Save!"



class RemoveSessionAction (BaseAction):
    """
    Действие для удаления сессии
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Sessions_RemoveSession"


    @property
    def title (self):
        return _(u"Remove session...")


    @property
    def description (self):
        return _(u"Remove session")


    def run (self, params):
        print "Remove!"

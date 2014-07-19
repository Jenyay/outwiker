# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class RemoveSessionAction (BaseAction):
    """
    Действие для удаления сессии
    """
    def __init__ (self, application, guicreator):
        self._application = application
        self._guicreator = guicreator

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

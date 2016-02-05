# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class OrgAction (BaseAction):
    """
    Описание действия
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Organizer_org"


    @property
    def title (self):
        return _(u"Insert (:org:) command")


    @property
    def description (self):
        return _(u"Description")


    def run (self, params):
        print "Run!"

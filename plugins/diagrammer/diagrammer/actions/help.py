# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getOS

from ..i18n import get_


class HelpAction (BaseAction):
    """
    Открыть справку по blockdiag
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Diagrammer_Help"


    @property
    def title (self):
        return _(u"Online Help")


    @property
    def description (self):
        return _(u"Diagrammer. Go to blockdiag webpage")


    def run (self, params):
        getOS().startFile (u"http://blockdiag.com/en/blockdiag/index.html")

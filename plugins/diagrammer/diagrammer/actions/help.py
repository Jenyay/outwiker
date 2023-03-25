# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction
from outwiker.api.services.application import startFile

from ..i18n import get_


class HelpAction(BaseAction):
    """
    Открыть справку по blockdiag
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "Diagrammer_Help"

    @property
    def title(self):
        return _("Online Help")

    @property
    def description(self):
        return _("Diagrammer. Go to blockdiag webpage")

    def run(self, params):
        startFile("http://blockdiag.com/en/blockdiag/index.html")

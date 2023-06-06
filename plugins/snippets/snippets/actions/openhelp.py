# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction

from snippets.i18n import get_
from snippets.utils import openHelp


class OpenHelpAction(BaseAction):
    stringId = "snippets_open_help"

    def __init__(self, application):
        super(OpenHelpAction, self).__init__()
        global _
        _ = get_()

    def run(self, params):
        openHelp()

    @property
    def title(self):
        return _("Open help...")

    @property
    def description(self):
        return _("Snippets. Open plugin help.")

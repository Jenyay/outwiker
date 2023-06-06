# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction

from .i18n import get_


class PluginAction(BaseAction):
    """
    Описание действия
    """

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "PluginName_Action"

    @property
    def title(self):
        return _("Menu Item Title")

    @property
    def description(self):
        return _("Description")

    def run(self, params):
        print("Run!")

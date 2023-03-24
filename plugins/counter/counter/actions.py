# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction
from .i18n import get_


class InsertCounterAction(BaseAction):
    """
    Вызвать диалог для вставки команды (:counter:)
    """
    stringId = "Counter_InsertCounter"

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    @property
    def title(self):
        return _("Counter (:counter ...:)")

    @property
    def description(self):
        return _("Counter plugin. Insert (:counter... :) command")

    def run(self, params):
        self._controller.insertCommand()

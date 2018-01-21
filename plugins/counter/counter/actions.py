# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class InsertCounterAction(BaseAction):
    """
    Вызвать диалог для вставки команды (:counter:)
    """
    stringId = u"Counter_InsertCounter"

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Counter (:counter ...:)")

    @property
    def description(self):
        return _(u"Counter plugin. Insert (:counter... :) command")

    def run(self, params):
        self._controller.insertCommand()

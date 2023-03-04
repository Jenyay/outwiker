# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class SaveAction(BaseAction):
    """
    Сохранить заметку
    """
    stringId = "SaveNote"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Save")

    @property
    def description(self):
        return _("Save current note")

    def run(self, params):
        self._application.onForceSave()

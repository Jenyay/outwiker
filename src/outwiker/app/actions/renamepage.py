# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class RenamePageAction(BaseAction):
    """
    Переименование страницы
    """
    stringId = "RenamePage"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Rename Page")

    @property
    def description(self):
        return _("Rename current page")

    def run(self, params):
        self._application.mainWindow.treePanel.beginRename()

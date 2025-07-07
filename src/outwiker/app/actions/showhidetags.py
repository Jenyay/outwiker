# -*- coding: utf-8 -*-

from outwiker.app.gui.mainwindowtools import showHideTagsPanel
from outwiker.gui.baseaction import BaseAction


class ShowHideTagsAction(BaseAction):
    """
    Показать / скрыть панель с тегами
    """
    stringId = "ShowHideTags"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Tags")

    @property
    def description(self):
        return _("Show / hide a tags panel")

    def run(self, params):
        showHideTagsPanel(self._application.mainWindow, params)

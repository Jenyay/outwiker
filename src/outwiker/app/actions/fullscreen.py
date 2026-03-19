# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class FullScreenAction(BaseAction):
    """
    Переход в полноэкранный режим и обратно
    """

    stringId = "Fullscreen"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Fullscreen")

    @property
    def description(self):
        return _("Toggle fullscreen mode")

    def run(self, params):
        self._application.mainWindow.setFullscreen(params)

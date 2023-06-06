# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction

from .i18n import get_


class SpoilerAction(BaseAction):
    """
    Описание действия
    """

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "Spoiler_Spoiler"

    @property
    def title(self):
        return _("(:spoiler:) Command")

    @property
    def description(self):
        return _("Insert (:spoiler:) wiki command")

    def run(self, params):
        startCommand = "(:spoiler:)"
        endCommand = "(:spoilerend:)"

        pageView = self._getPageView()
        pageView.codeEditor.turnText(startCommand, endCommand)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

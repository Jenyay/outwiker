# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction

from .i18n import get_


class SpoilerAction (BaseAction):
    """
    Описание действия
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Spoiler_Spoiler"

    @property
    def title(self):
        return _(u"(:spoiler:) Command")

    @property
    def description(self):
        return _(u"Insert (:spoiler:) wiki command")

    def run(self, params):
        startCommand = u'(:spoiler:)'
        endCommand = u'(:spoilerend:)'

        pageView = self._getPageView()
        pageView.codeEditor.turnText(startCommand, endCommand)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

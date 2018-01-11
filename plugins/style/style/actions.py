# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class StyleAction (BaseAction):
    """
    Описание действия
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Style_Style"

    @property
    def title(self):
        return _(u"Custom Style (:style:)")

    @property
    def description(self):
        return _(u"Insert (:style:) wiki command to use a custom CSS style")

    def run(self, params):
        startCommand = u'(:style:)\n'
        endCommand = u'\n(:styleend:)'

        pageView = self._getPageView()
        pageView.codeEditor.turnText(startCommand, endCommand)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

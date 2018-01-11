# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class LightboxAction(BaseAction):
    """
    Описание действия
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Lightbox_Lightbox"

    @property
    def title(self):
        return _(u"(:lightbox:) command")

    @property
    def description(self):
        return _(u"Insert (:lightbox:) wiki command to show attached images inside OutWiker.")

    def run(self, params):
        command = u'(:lightbox:)'

        pageView = self._getPageView()
        pageView.codeEditor.replaceText(command)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

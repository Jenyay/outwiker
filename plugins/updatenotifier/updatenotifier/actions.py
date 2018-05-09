# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class CheckForUpdatesAction(BaseAction):
    """
    Проверка обновлений
    """
    stringId = u"UpdateNotifier_CheckForUpdates"

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Check for Updates...")

    @property
    def description(self):
        return _(u"UpdateNotifier plugin. Check for updates")

    def run(self, params):
        self._controller.checkForUpdates()


class CheckForUpdatesSilenceAction(BaseAction):
    """
    Проверка обновлений. Тихий режим
    """
    stringId = u"UpdateNotifier_CheckForUpdatesSilence"

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Silence check for Updates...")

    @property
    def description(self):
        return _(u"UpdateNotifier plugin. Check for updates. Silence mode")

    def run(self, params):
        self._controller.checkForUpdatesSilence()

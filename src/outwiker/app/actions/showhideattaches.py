# -*- coding: utf-8 -*-

from .showhidebase import ShowHideBaseAction


class ShowHideAttachesAction(ShowHideBaseAction):
    """
    Показать / скрыть панель с прикрепленными файлами
    """
    stringId = "ShowHideAttaches"

    def __init__(self, application):
        super(ShowHideAttachesAction, self).__init__(application)

    @property
    def title(self):
        return _("Attachments")

    @property
    def description(self):
        return _("Show / hide a attachments panel")

    def getPanel(self):
        return self._application.mainWindow.attachPanel

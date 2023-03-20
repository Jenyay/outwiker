# -*- coding: utf-8 -*-

from outwiker.api.gui.mainwindow import showHideAttachPanel
from outwiker.gui.baseaction import BaseAction


class ShowHideAttachesAction(BaseAction):
    """
    Показать / скрыть панель с прикрепленными файлами
    """
    stringId = "ShowHideAttaches"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Attachments")

    @property
    def description(self):
        return _("Show / hide a attachments panel")

    def run(self, params):
        showHideAttachPanel(self._application, params)

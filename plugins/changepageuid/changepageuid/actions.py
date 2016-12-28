# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from changepageuid.utils import changeUidWithDialog
from changepageuid.i18n import get_


class ChangePageUIDAction(BaseAction):
    """
    Описание действия
    """
    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = u"ChangePageUID_ChangePageUID"

    @property
    def title(self):
        return _(u"Change Page Identifier...")

    @property
    def description(self):
        return _(u"ChangePageUID plugin. Change Page Identifier")

    def run(self, params):
        changeUidWithDialog(self._application.selectedPage, self._application)

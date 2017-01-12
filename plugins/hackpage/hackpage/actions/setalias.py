# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from hackpage.utils import setAliasWithDialog
from hackpage.i18n import get_


class SetAliasAction(BaseAction):
    """
    Описание действия
    """
    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = u"HackPage_SetAlias"

    @property
    def title(self):
        return _(u"Set page alias...")

    @property
    def description(self):
        return _(u"HackPage plugin. Set page alias")

    def run(self, params):
        setAliasWithDialog(self._application.selectedPage, self._application)

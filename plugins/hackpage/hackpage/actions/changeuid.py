from outwiker.api.gui.actions import BaseAction

from hackpage.utils import changeUidWithDialog
from hackpage.i18n import get_


class ChangeUIDAction(BaseAction):
    """
    Описание действия
    """

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = "HackPage_ChangePageUID"

    @property
    def title(self):
        return _("Change Page Identifier...")

    @property
    def description(self):
        return _("HackPage plugin. Change Page Identifier")

    def run(self, params):
        changeUidWithDialog(self._application.selectedPage, self._application)

from outwiker.api.gui.actions import BaseAction

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

    stringId = "HackPage_SetAlias"

    @property
    def title(self):
        return _("Set page alias...")

    @property
    def description(self):
        return _("HackPage plugin. Set page alias")

    def run(self, params):
        setAliasWithDialog(self._application.selectedPage, self._application)

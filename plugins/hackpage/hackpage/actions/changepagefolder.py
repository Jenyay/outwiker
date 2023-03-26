from outwiker.api.gui.actions import BaseAction

from hackpage.utils import setPageFolderWithDialog
from hackpage.i18n import get_


class ChangePageFolderAction(BaseAction):
    """
    Change the current page folder (title)
    """

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = "HackPage_ChangePageFolder"

    @property
    def title(self):
        return _("Change page folder...")

    @property
    def description(self):
        return _("HackPage plugin. Change the current page folder")

    def run(self, params):
        setPageFolderWithDialog(self._application.selectedPage, self._application)

from outwiker.gui.baseaction import BaseAction

from hackpage.utils import setPageCreationDate
from hackpage.i18n import get_


class ChangePageCreationDateAction(BaseAction):
    """
    Change page creation date and time
    """

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = "HackPage_ChangePageCreationDate"

    @property
    def title(self):
        return _("Change page creation date and time...")

    @property
    def description(self):
        return _("HackPage plugin. Change page creation date and time")

    def run(self, params):
        setPageCreationDate(self._application.selectedPage, self._application)

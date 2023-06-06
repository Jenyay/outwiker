from outwiker.api.gui.actions import BaseAction

from hackpage.utils import setPageChangeDate
from hackpage.i18n import get_


class ChangePageChangeDateAction(BaseAction):
    """
    Change date and time of change of the page
    """

    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = "HackPage_ChangePageChangeDate"

    @property
    def title(self):
        return _("Change date and time of change of the page...")

    @property
    def description(self):
        return _("HackPage plugin. Change date and time of change of the page")

    def run(self, params):
        setPageChangeDate(self._application.selectedPage, self._application)

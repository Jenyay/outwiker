from outwiker.app.gui.mainwindowtools import showHideBookmarksPanel
from outwiker.gui.baseaction import BaseAction


class ShowHideBookmarksAction(BaseAction):
    """Show / hide bookmark panel"""

    stringId = "BookmarkManagement"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Bookmark management...")

    @property
    def description(self):
        return _("Show the dialog for bookmark management")

    def run(self, params):
        if self._application.mainWindow is not None:
            showHideBookmarksPanel(self._application.mainWindow, params)

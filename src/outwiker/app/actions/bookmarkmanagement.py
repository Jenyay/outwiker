from outwiker.gui.baseaction import BaseAction


class BookmarkManagementAction(BaseAction):
    """Show dialog for bookmarks edit"""

    stringId = "BookmarkManagement"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Bookmark management...")

    @property
    def description(self):
        return _("Show the dialog for bookmarks management")

    def run(self, params):
        if self._application.mainWindow is not None:
            self._application.mainWindow.showBookmarkManagementDialog()

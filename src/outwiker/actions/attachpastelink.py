# -*- coding=utf-8 -*-

from outwiker.core.commands import showError
from outwiker.gui.baseaction import BaseAction


class AttachPasteLinkActionForAttachPanel(BaseAction):
    """
    Insert link to selected files to editor.
    """
    stringId = "AttachPasteLink"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Insert link to attached files")

    @property
    def description(self):
        return _("Insert link to attached file")

    def run(self, params):
        attachPanel = self._application.mainWindow.attachPanel.panel
        files = attachPanel.getSelectedFiles()
        if len(files) == 0:
            showError(self._application.mainWindow,
                      _("You did not select any attached file"))
            return

        self._application.onAttachmentPaste(files)

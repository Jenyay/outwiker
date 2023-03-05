# -*- coding=utf-8 -*-

import os.path

from outwiker.api.services.messages import showError
from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS
from outwiker.gui.baseaction import BaseAction


class AttachExecuteFilesAction(BaseAction):
    """
    Execute selected files action
    """
    stringId = "AttachExecuteFiles"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Execute files")

    @property
    def description(self):
        return _("Execute selected attached files")

    def run(self, params):
        attachPanel = self._application.mainWindow.attachPanel.panel
        if self._application.selectedPage is not None:
            files = attachPanel.getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _("You did not select a file to execute"))
                return

            for file in files:
                fullpath = os.path.join(Attachment(
                    self._application.selectedPage).getAttachPath(), file)
                try:
                    getOS().startFile(fullpath)
                except OSError:
                    text = _("Can't execute file '%s'") % file
                    showError(self._application.mainWindow, text)

# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import showError
from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


class OpenAttachFolderAction(BaseAction):
    """
    Открыть папку с прикрепленными файлами в системном файловом менеджере
    """
    stringId = "OpenAttachFolder"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Open Attachments Folder")

    @property
    def description(self):
        return _("Open folder with attached files")

    def run(self, page=None):
        if page is None:
            page = self._application.selectedPage

        if page is None:
            return

        if page is not None:
            folder = Attachment(page).getAttachPath(create=True)
            try:
                getOS().startFile(folder)
            except OSError:
                text = _("Can't open folder '{}'".format(folder))
                showError(self._application.mainWindow, text)


class OpenAttachFolderActionForAttachPanel(OpenAttachFolderAction):
    stringId = "OpenAttachFolderForAttachPanel"

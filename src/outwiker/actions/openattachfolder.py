# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import showError
from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


class OpenAttachFolderAction (BaseAction):
    """
    Открыть папку с прикрепленными файлами в системном файловом менеджере
    """
    stringId = u"OpenAttachFolder"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Open Attachments Folder")

    @property
    def description(self):
        return _(u"Open folder with attached files")

    def run(self, params):
        if self._application.selectedPage is not None:
            folder = Attachment(
                self._application.selectedPage).getAttachPath(create=True)
            try:
                getOS().startFile(folder)
            except OSError:
                text = _(u"Can't open folder '{}'".format(folder))
                showError(self._application.mainWindow, text)

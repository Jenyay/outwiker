# -*- coding=utf-8 -*-

from outwiker.core.events import BeginAttachRenamingParams
from outwiker.gui.baseaction import BaseAction


class RenameAttachActionForAttachPanel(BaseAction):
    """
    Begin renaming selected attached file
    """
    stringId = "AttachRename"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Rename attachment")

    @property
    def description(self):
        return _("Rename selected attached file. Action for attachments panel")

    def run(self, params):
        self._application.onBeginAttachRenaming(
            self._application.selectedPage, BeginAttachRenamingParams())

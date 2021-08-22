# -*- coding=utf-8 -*-

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
        if self._application.selectedPage is not None:
            attachPanel = self._application.mainWindow.attachPanel.panel
            attachPanel.beginRenaming()

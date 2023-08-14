# -*- coding=utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class AttachSelectAllAction(BaseAction):
    """
    Select all attachments on attachments panel
    """
    stringId = "AttachSelectAll"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Select all")

    @property
    def description(self):
        return _("Select all attachments. Action for the attachments panel")

    def run(self, params):
        self._application.mainWindow.attachPanel.panel.selectAllAttachments()

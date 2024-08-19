# coding: utf-8

import wx

from outwiker.app.services.messages import showError
from outwiker.core.attachment import Attachment
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.dialogs.messagebox import MessageBox


class RemoveAttachesActionForAttachPanel(BaseAction):
    """
    Remove attachments.

    Hidden action.
    """
    stringId = "RemoveAttachesForAttachPanel"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Remove attachments")

    @property
    def description(self):
        return _("Remove selected attachments. Action for attach panel")

    def run(self, params):
        attachPanel = self._application.mainWindow.attachPanel.panel

        if self._application.selectedPage is not None:
            files = attachPanel.getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _("You did not select any attachment to remove"))
                return

            files_str = '\n'.join(files)
            text = _("Remove selected attachments?") + '\n\n' + files_str

            if MessageBox(text,
                          _("Removing attachments"),
                          wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                try:
                    Attachment(
                        self._application.selectedPage).removeAttach(files)
                except IOError as e:
                    showError(self._application.mainWindow, str(e))

                attachPanel.updateAttachments()

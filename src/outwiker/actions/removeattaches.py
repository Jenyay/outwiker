# coding: utf-8

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.attachment import Attachment
from outwiker.core.commands import MessageBox, showError


class RemoveAttachesActionForAttachPanel(BaseAction):
    """
    Remove attached files.

    Hidden action.
    """
    stringId = "RemoveAttachesForAttachPanel"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Remove attached files")

    @property
    def description(self):
        return _("Remove attached files. Action for attach panel")

    def run(self, params):
        attachPanel = self._application.mainWindow.attachPanel.panel

        if self._application.selectedPage is not None:
            files = attachPanel.getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _("You did not select any file to remove"))
                return

            if MessageBox(_("Remove selected files?"),
                          _("Remove files?"),
                          wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                try:
                    Attachment(
                        self._application.selectedPage).removeAttach(files)
                except IOError as e:
                    showError(self._application.mainWindow, str(e))

                attachPanel.updateAttachments()

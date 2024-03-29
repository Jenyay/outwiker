# -*- coding: utf-8 -*-

from io import StringIO

import wx

from ..config import ExternalToolsConfig
from ..commandexec.commandparams import TITLE_NAME, FORMAT_NAME, FORMAT_BUTTON


class ExecDialogController:
    def __init__(self, dialog, application):
        self._dialog = dialog
        self._application = application
        self._config = ExternalToolsConfig(self._application.config)
        self._loadState()

    def showDialog(self):
        """
        The method shows dialog and return result of the ShowModal method
        """
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._saveState()

        return result

    def _loadState(self):
        """
        Load settings from config
        """
        self._updateDialogSize()
        self._dialog.format = self._config.execFormat

    def _updateDialogSize(self):
        """
        Set dialog size
        """
        currentWidth, currentHeight = self._dialog.GetClientSize()
        dialogWidth = max(self._config.dialogWidth, currentWidth)
        dialogHeight = max(self._config.dialogHeight, currentHeight)

        self._dialog.SetClientSize(dialogWidth, dialogHeight)

    def _saveState(self):
        """
        Save settings to config
        """
        currentWidth, currentHeight = self._dialog.GetClientSize()
        self._config.dialogWidth = currentWidth
        self._config.dialogHeight = currentHeight
        self._config.execFormat = self._dialog.format

    def getResult(self):
        """
        Return tuple:(begin command, end command)
        """
        openCommand = StringIO()
        openCommand.write("(:exec")

        if self._dialog.title:
            openCommand.write(' {}="{}"'.format(TITLE_NAME, self._dialog.title))

        if self._dialog.format == 1:
            openCommand.write(' {}="{}"'.format(FORMAT_NAME, FORMAT_BUTTON))

        openCommand.write(":)")

        closeComamnd = "(:execend:)"

        return (openCommand.getvalue(), closeComamnd)

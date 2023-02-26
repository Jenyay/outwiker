# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.dialogs.messagebox import MessageBox
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.guiconfig import GeneralGuiConfig


class ExitAction (BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = "Exit"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Exit…")

    @property
    def description(self):
        return _("Close OutWiker")

    def run(self, params):
        if (self.__allowExit()):
            self._application.mainWindow.Destroy()

    def __allowExit(self):
        """
        Return True, if the window can be closed
        """
        generalConfig = GeneralGuiConfig(self._application.config)
        askBeforeExit = generalConfig.askBeforeExit.value

        return (not askBeforeExit or
                MessageBox(_("Really exit?"),
                           _("Exit"),
                           wx.YES_NO | wx.ICON_QUESTION) == wx.YES)

# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.dialogs.messagebox import MessageBox
from outwiker.gui.guiconfig import GeneralGuiConfig


def exit(application):
    def _allow_exit(application) -> bool:
        """
        Return True, if the window can be closed
        """
        generalConfig = GeneralGuiConfig(application.config)
        askBeforeExit = generalConfig.askBeforeExit.value

        return (not askBeforeExit or
                MessageBox(_("Really exit?"),
                           _("Exit"),
                           wx.YES_NO | wx.ICON_QUESTION) == wx.YES)

    if (_allow_exit(application)):
        application.mainWindow.Destroy()



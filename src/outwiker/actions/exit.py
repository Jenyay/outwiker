# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import MessageBox


class ExitAction (BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = u"Exit"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Exit…")


    @property
    def description (self):
        return _(u"Close OutWiker")


    def run (self, params):
        if (self.__allowExit()):
            self._application.mainWindow.Destroy()
            wx.Exit()


    def __allowExit (self):
        """
        Возвращает True, если можно закрывать окно
        """
        generalConfig = GeneralGuiConfig(self._application.config)
        askBeforeExit = generalConfig.askBeforeExit.value

        return (not askBeforeExit or
                MessageBox (_(u"Really exit?"),
                            _(u"Exit"),
                            wx.YES_NO | wx.ICON_QUESTION) == wx.YES)

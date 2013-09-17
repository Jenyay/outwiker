#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys

import wxversion

try:
    wxversion.select("2.8")
except wxversion.VersionError:
    if os.name == "nt":
        pass
    else:
        raise

import wx

from outwiker.core.application import Application
from outwiker.core.system import getOS, getPluginsDirList, getConfigPath
from outwiker.core.starter import Starter
from outwiker.gui.wxactioncontroller import WxActionController

from outwiker.actions.new import NewAction
from outwiker.actions.open import OpenAction
from outwiker.actions.openreadonly import OpenReadOnlyAction
from outwiker.actions.close import CloseAction
from outwiker.actions.save import SaveAction
from outwiker.actions.printaction import PrintAction


class OutWiker(wx.App):
    def __init__(self, *args, **kwds):
        self.logFileName = u"outwiker.log"

        wx.App.__init__ (self, *args, **kwds)


    def OnInit(self):
        self._fullConfigPath = getConfigPath ()
        Application.init(self._fullConfigPath)

        # Если программа запускается в виде exe-шника, то перенаправить вывод ошибок в лог
        exepath = unicode (sys.argv[0], getOS().filesEncoding)
        if exepath.endswith (u".exe"):
            # Закоментировать следующую строку, если не надо выводить strout/strerr в лог-файл
            self.RedirectStdio (self.getLogFileName (self._fullConfigPath))
            pass

        from outwiker.gui.mainwindow import MainWindow
        
        wx.InitAllImageHandlers()
        self.mainWnd = MainWindow(None, -1, "")
        self.SetTopWindow (self.mainWnd)

        Application.mainWindow = self.mainWnd
        Application.actionController = WxActionController (self.mainWnd)

        self._registerActions()
        self.mainWnd.addActionsGui()

        Application.plugins.load (getPluginsDirList())

        self.bindActivateApp()
        self.Bind (wx.EVT_QUERY_END_SESSION, self._onEndSession)

        starter = Starter()
        starter.process()
        
        return True


    def _registerActions (self):
        """
        Зарегистрировать действия, связанные с разными типами страниц
        """
        from outwiker.pages.html.htmlpage import HtmlPageFactory
        HtmlPageFactory.registerActions (Application)

        # Открыть...
        Application.actionController.register (OpenAction (Application), "Ctrl+O")

        # Создать...
        Application.actionController.register (NewAction (Application), "Ctrl+N")

        # Открыть только для чтения
        Application.actionController.register (OpenReadOnlyAction (Application), "Ctrl+Shift+O")
        
        # Закрыть
        Application.actionController.register (CloseAction (Application), "Ctrl+Shift+W")

        # Сохранить
        Application.actionController.register (SaveAction (Application), "Ctrl+S")

        # Печать
        Application.actionController.register (PrintAction (Application), "Ctrl+P")


    def _onEndSession (self, event):
        self.mainWnd.Destroy()


    def getLogFileName (self, configPath):
        return os.path.join (os.path.split (configPath)[0], self.logFileName)


    def bindActivateApp (self):
        """
        Подключиться к событию при потере фокуса приложением
        """
        self.Bind (wx.EVT_ACTIVATE_APP, self.onActivate)


    def unbindActivateApp (self):
        """
        Отключиться от события при потере фокуса приложением
        """
        self.Unbind (wx.EVT_ACTIVATE_APP)


    def onActivate (self, event):
        Application.onForceSave()


# end of class OutWiker

if __name__ == "__main__":
    getOS().init()
    outwiker = OutWiker(False)
    outwiker.MainLoop()

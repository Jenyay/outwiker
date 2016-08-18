#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import logging

from outwiker.core.defines import WX_VERSION, APP_DATA_DEBUG
import wxversion

try:
    wxversion.select(WX_VERSION)
except wxversion.VersionError:
    if(sys.argv[0].endswith('outwiker') or
            sys.argv[0].endswith('outwiker.exe')):
        pass
    else:
        raise

import wx

from outwiker.core.application import Application
from outwiker.core.system import getOS, getPluginsDirList, getConfigPath
from outwiker.core.starter import Starter, StarterExit
from outwiker.core.commands import registerActions
from outwiker.core.logredirector import LogRedirector
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.guiconfig import GeneralGuiConfig


class OutWiker(wx.App):
    """
    OutWiker application class
    """
    def __init__(self, *args, **kwds):
        self.logFileName = u"outwiker.log"
        self._locale = None

        wx.App.__init__(self, *args, **kwds)

    def OnInit(self):
        getOS().init()
        getOS().migrateConfig()

        self._fullConfigPath = getConfigPath()
        Application.init(self._fullConfigPath)
        self._locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        try:
            starter = Starter()
            starter.processConsole()
        except StarterExit:
            return True

        config = GeneralGuiConfig(Application.config)
        Application.sharedData[APP_DATA_DEBUG] = config.debug.value
        level = (logging.INFO
                 if Application.sharedData[APP_DATA_DEBUG]
                 else logging.WARNING)

        redirector = LogRedirector(self.getLogFileName(self._fullConfigPath),
                                   level)
        redirector.init()
        wx.Log.SetLogLevel(0)

        from outwiker.gui.mainwindow import MainWindow

        self.mainWnd = MainWindow(None, -1, "")
        self.SetTopWindow(self.mainWnd)

        Application.mainWindow = self.mainWnd
        Application.actionController = ActionController(self.mainWnd,
                                                        Application.config)

        registerActions(Application)
        self.mainWnd.createGui()

        Application.plugins.load(getPluginsDirList())

        self.bindActivateApp()
        self.Bind(wx.EVT_QUERY_END_SESSION, self._onEndSession)

        starter.processGUI()

        return True

    def _onEndSession(self, event):
        self.mainWnd.Destroy()

    def getLogFileName(self, configPath):
        return os.path.join(os.path.split(configPath)[0], self.logFileName)

    def bindActivateApp(self):
        """
        Подключиться к событию при потере фокуса приложением
        """
        self.Bind(wx.EVT_ACTIVATE_APP, self._onActivate)

    def unbindActivateApp(self):
        """
        Отключиться от события при потере фокуса приложением
        """
        self.Unbind(wx.EVT_ACTIVATE_APP)

    def _onActivate(self, event):
        Application.onForceSave()


if __name__ == "__main__":
    outwiker = OutWiker(False)
    outwiker.MainLoop()

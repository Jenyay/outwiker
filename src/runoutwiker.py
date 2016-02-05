#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys

from outwiker.core.defines import WX_VERSION
import wxversion

try:
    wxversion.select(WX_VERSION)
except wxversion.VersionError:
    if (sys.argv[0].endswith (u'outwiker') or
            sys.argv[0].endswith (u'outwiker.exe')):
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


class OutWiker(wx.App):
    def __init__(self, *args, **kwds):
        self.logFileName = u"outwiker.log"

        wx.App.__init__ (self, *args, **kwds)


    def OnInit (self):
        getOS().migrateConfig()
        self._fullConfigPath = getConfigPath ()
        Application.init(self._fullConfigPath)

        try:
            starter = Starter()
            starter.processConsole()
        except StarterExit:
            return True

        redirector = LogRedirector (self.getLogFileName (self._fullConfigPath))
        redirector.init()

        from outwiker.gui.mainwindow import MainWindow

        self.mainWnd = MainWindow(None, -1, "")
        self.SetTopWindow (self.mainWnd)

        Application.mainWindow = self.mainWnd
        Application.actionController = ActionController (self.mainWnd, Application.config)

        registerActions(Application)
        self.mainWnd.createGui()

        Application.plugins.load (getPluginsDirList())

        self.bindActivateApp()
        self.Bind (wx.EVT_QUERY_END_SESSION, self._onEndSession)

        starter.processGUI()

        return True


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys

#import wxversion
#wxversion.select("2.8")

import wx

from outwiker.core.application import Application
from outwiker.core.system import getOS, getPluginsDirList, getConfigPath
from outwiker.core.starter import Starter


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

        from outwiker.gui.MainWindow import MainWindow
        
        wx.InitAllImageHandlers()
        self.mainWnd = MainWindow(None, -1, "")
        self.SetTopWindow (self.mainWnd)
        Application.mainWindow = self.mainWnd
        Application.plugins.load (getPluginsDirList())

        self.bindActivateApp()

        starter = Starter()
        starter.process()
        
        return 1


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
        if not event.GetActive():
            Application.onForceSave()


# end of class OutWiker

if __name__ == "__main__":
    getOS().init()
    outwiker = OutWiker(False)
    outwiker.MainLoop()

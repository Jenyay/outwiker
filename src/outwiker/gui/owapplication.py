# -*- coding: utf-8 -*-

import os
import os.path
import logging
from gettext import NullTranslations

import wx
import wx.html

from outwiker.core.commands import registerActions
from outwiker.core.logredirector import LogRedirector
from outwiker.core.system import getPluginsDirList
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.guiconfig import TrayConfig, TextPrintConfig
from outwiker.gui.mainwindow import MainWindow


class OutWikerApplication(wx.App):
    """
    OutWiker application class
    """
    def __init__(self, application):
        super().__init__()
        self.logFileName = u"outwiker.log"
        self._application = application

        config = TextPrintConfig(self._application.config)
        self.normalFont = config.fontName.value
        self.monoFont = config.fontName.value

    def OnInit(self):
        self.Bind(wx.EVT_QUERY_END_SESSION, self._onEndSession)
        NullTranslations().install()
        return True

    def initMainWindow(self):
        self.mainWnd = MainWindow(self._application)
        self.SetTopWindow(self.mainWnd)

        self._application.mainWindow = self.mainWnd
        self._application.actionController = ActionController(
            self.mainWnd, self._application.config)

        registerActions(self._application)
        self.mainWnd.createGui()
        self.initPrinting()

    def initPrinting(self):
        self.printing = wx.html.HtmlEasyPrinting(parentWindow=self.mainWnd)
        self.printing.SetFonts(self.normalFont,
                               self.monoFont,
                               list(range(10, 17)))

    def destroyMainWindow(self):
        self.mainWnd.Destroy()
        self.mainWnd = None
        self._application.mainWindow = None
        self._application = None

    def loadPlugins(self):
        self._application.plugins.load(getPluginsDirList())

    def showMainWindow(self, allowMinimizingMainWindow=True):
        config = TrayConfig(self._application.config)
        if config.startIconized.value and allowMinimizingMainWindow:
            self.mainWnd.Iconize(True)
        else:
            self.mainWnd.Show()

        self.mainWnd.taskBarIconController.updateTrayIcon()

    def initLogger(self, debugMode=False):
        level = logging.DEBUG if debugMode else logging.WARNING

        redirector = LogRedirector(
            self.getLogFileName(self._application.fullConfigPath),
            level)

        redirector.init()
        wx.Log.SetLogLevel(0)

    def _onEndSession(self, event):
        self.Unbind(wx.EVT_QUERY_END_SESSION, handler=self._onEndSession)
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
        self._application.onForceSave()

    @property
    def application(self):
        return self._application

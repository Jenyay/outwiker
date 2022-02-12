# -*- coding: utf-8 -*-

import locale
import logging
import os
import os.path
import sys
from gettext import NullTranslations

import wx

from outwiker.core.logredirector import LogRedirector
from outwiker.core.system import getPluginsDirList
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.guiconfig import TrayConfig
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.polyaction import PolyAction


class OutWikerApplication(wx.App):
    """
    OutWiker application class
    """

    def __init__(self, application):
        super().__init__()
        self._initLocale()

        self.logFileName = u"outwiker.log"
        self._application = application

        self.use_fake_html_render = False

    def _initLocale(self):
        # Fix a locale problem with Python 3.8 and wxPython 4.1
        if sys.platform.startswith('win'):
            locale.setlocale(locale.LC_ALL, 'C')

    def OnInit(self):
        self.Bind(wx.EVT_QUERY_END_SESSION, self._onEndSession)
        NullTranslations().install()
        return True

    def initMainWindow(self):
        self._initLocale()
        self.mainWnd = MainWindow(self._application)
        self.SetTopWindow(self.mainWnd)

        self._application.mainWindow = self.mainWnd
        self._application.actionController = ActionController(
            self.mainWnd, self._application.config)

        self._registerActions(self._application)
        self.mainWnd.createGui()

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

    def _registerActions(self, application):
        """
        Зарегистрировать действия
        """
        # Действия, связанные с разными типами страниц
        from outwiker.pages.html.htmlpage import HtmlPageFactory
        HtmlPageFactory.registerActions(application)

        from outwiker.pages.wiki.wikipage import WikiPageFactory
        WikiPageFactory.registerActions(application)

        actionController = application.actionController
        from outwiker.gui.actionslist import actionsList, polyactionsList

        # Register the normal actions
        [actionController.register(item.action_type(application),
                                   item.hotkey,
                                   item.area,
                                   item.hidden)
         for item in actionsList]

        # Register the polyactions
        [actionController.register(PolyAction(application,
                                              item.stringId,
                                              item.title,
                                              item.description),
                                   item.hotkey) for item in polyactionsList]

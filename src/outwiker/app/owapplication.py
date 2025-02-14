# -*- coding: utf-8 -*-

import locale
import logging
import os
import os.path
import sys
from gettext import NullTranslations
from typing import Optional

import wx

from outwiker.app.core.logredirector import LogRedirector
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.i18n import initLocale
from outwiker.core.init import init_page_factories
from outwiker.core.system import getPluginsDirList
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.guiconfig import TrayConfig
from outwiker.gui.polyaction import PolyAction


class OutWikerApplication(wx.App):
    """
    OutWiker application class
    """

    def __init__(self, application):
        super().__init__()

        self.logFileName = 'outwiker.log'
        self._application = application
        self.use_fake_html_render = False
        self.enableActionsGui = True

        self._locale = initLocale(self._application.config)
        self._initLocale()
        init_page_factories()

    def _initLocale(self):
        # Fix a locale problem with Python 3.8 and wxPython 4.1
        # Overwrite InitLocale from the wx.App class
        locale.setlocale(locale.LC_ALL, '')
        if sys.platform.startswith('win'):
            # Very dirty hack
            try:
                wx.Locale.GetInfo(wx.LOCALE_DECIMAL_POINT)
            except Exception:
                locale.setlocale(locale.LC_ALL, 'C')

    def OnInit(self):
        NullTranslations().install()
        return True

    def getMainWindow(self) -> Optional[MainWindow]:
        return self._mainWindow

    def initMainWindow(self):
        self._initLocale()
        self._application.theme.loadSystemParams()
        self._application.theme.loadFromConfig(self._application.config)
        self._mainWindow = MainWindow(self._application)
        self.SetTopWindow(self._mainWindow)

        self._application.mainWindow = self._mainWindow
        self._application.actionController = ActionController(
            self._mainWindow, self._application.config)
        self._application.actionController.enableGui(self.enableActionsGui)

        self._registerActions(self._application)
        self._mainWindow.createGui()

    def destroyMainWindow(self):
        self._mainWindow.Destroy()
        self._mainWindow = None
        self._application.mainWindow = None
        self._application = None

    def loadPlugins(self):
        self._application.plugins.load(getPluginsDirList())

    def showMainWindow(self, allowMinimizingMainWindow=True):
        config = TrayConfig(self._application.config)

        if config.startIconized.value and allowMinimizingMainWindow:
            self._mainWindow.hideToTray()
        else:
            self._mainWindow.Show()

        self._mainWindow.updateTrayIcon()

    def initLogger(self, debugMode=False):
        level = logging.DEBUG if debugMode else logging.WARNING

        redirector = LogRedirector(
            self.getLogFileName(self._application.fullConfigPath),
            level)

        redirector.init()
        wx.Log.SetLogLevel(0)

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
        from outwiker.app.gui.actionslist import actionsList, polyactionsList

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

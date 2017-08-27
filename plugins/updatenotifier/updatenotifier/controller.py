# -*- coding: utf-8 -*-

import datetime

import wx

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .i18n import get_
from .updatecontroller import UpdateController
from .preferencepanel import PreferencePanel
from .updatesconfig import UpdatesConfig
from .guicreators import OldGuiCreator, ActionGuiCreator


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__(self, plugin, application):
        """
        plugin - Instance of the PluginUpdateNotifier class
        application - Instance of the ApplicationParams class
        """
        self._plugin = plugin
        self._application = application

        # Add some new menu items in the debug mode
        self._debug = False
        self._updatesChecker = None

        self._guiCreator = None

    def initialize(self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        try:
            from outwiker.gui.baseaction import BaseAction
            self._guiCreator = ActionGuiCreator(self, self._application)
        except ImportError:
            self._guiCreator = OldGuiCreator(self, self._application)

        self._updatesChecker = UpdateController(self._application,
                                                self._plugin.pluginPath)

        self._guiCreator.initialize()

        if self._application.mainWindow is not None:
            self._application.mainWindow.Bind(wx.EVT_IDLE, handler=self.__onIdle)

        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._guiCreator.destroy()
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

    @property
    def debug(self):
        return self._debug

    def checkForUpdates(self):
        self._updatesChecker.checkForUpdates()

    def checkForUpdatesSilence(self):
        self._updatesChecker.checkForUpdatesSilence()

    def __onIdle(self, event):
        self.__autoUpdate()
        self._application.mainWindow.Unbind(wx.EVT_IDLE, handler=self.__onIdle)

    def __autoUpdate(self):
        """
        Автоматическая проверка обновлений
        """
        config = UpdatesConfig(self._application.config)

        if(config.updateInterval > 0 and
                datetime.datetime.today() - config.lastUpdate >= datetime.timedelta(config.updateInterval)):
            self.checkForUpdatesSilence()

    def __onPreferencesDialogCreate(self, dialog):
        """
        Добавление страницы с настройками
        """
        prefPanel = PreferencePanel(dialog.treeBook, self._application.config)

        panelName = _(u"UpdateNotifier [Plugin]")
        panelsList = [PreferencePanelInfo(prefPanel, panelName)]
        dialog.appendPreferenceGroup(panelName, panelsList)

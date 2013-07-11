#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import datetime

import wx

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .i18n import get_
from .updateschecker import UpdatesChecker
from .preferencepanel import PreferencePanel
from .updatesconfig import UpdatesConfig


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, application):
        """
        plugin - Владелец контроллера (экземпляр класса PluginSource)
        application - экземпляр класса ApplicationParams
        """
        self.UPDATE_ID = wx.NewId()
        self.SILENCE_UPDATE_ID = wx.NewId()
        self._application = application

        # В режиме отладки добавляются новые пункты меню
        self._debug = True
        self._updatesChecker = None


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._updatesChecker = UpdatesChecker (self._application)

        if self._application.mainWindow != None:
            self._application.mainWindow.Bind (wx.EVT_IDLE, handler=self.__onIdle)
            self.__createMenu()
        
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        if self._application.mainWindow != None:
            self._application.mainWindow.Unbind (wx.EVT_MENU, id=self.UPDATE_ID, handler=self.__onCheckUpdate)
            self._helpMenu.Delete (self.UPDATE_ID)

            if self._debug:
                self._helpMenu.Delete (self.SILENCE_UPDATE_ID)

        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate


    def __onIdle (self, event):
        self.__autoUpdate()
        self._application.mainWindow.Unbind (wx.EVT_IDLE, handler=self.__onIdle)


    def __autoUpdate (self):
        """
        Автоматическая проверка обновлений
        """
        config = UpdatesConfig (self._application.config)

        if (config.updateInterval > 0 and
                datetime.datetime.today() - config.lastUpdate  >= datetime.timedelta (config.updateInterval)):
            self._updatesChecker.checkForUpdatesSilence()



    def __createMenu (self):
        """Добавление пункта меню для проверки обновлений"""
        assert self._application.mainWindow != None

        self._helpMenu.Append (id=self.UPDATE_ID, text=_(u"Check for Updates..."))
        self._application.mainWindow.Bind (wx.EVT_MENU, self.__onCheckUpdate, id=self.UPDATE_ID)

        if self._debug:
            self._helpMenu.Append (id=self.SILENCE_UPDATE_ID, text=_(u"Silence check for Updates..."))
            self._application.mainWindow.Bind (wx.EVT_MENU, self.__onSilenceCheckUpdate, id=self.SILENCE_UPDATE_ID)


    def __onCheckUpdate (self, event):
        self._updatesChecker.checkForUpdates()


    def __onSilenceCheckUpdate (self, event):
        self._updatesChecker.checkForUpdatesSilence()


    def __onPreferencesDialogCreate (self, dialog):
        """
        Добавление страницы с настройками
        """
        prefPanel = PreferencePanel (dialog.treeBook, self._application.config)

        panelName = _(u"UpdateNotifier [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)


    @property
    def _helpMenu (self):
        return self._application.mainWindow.mainMenu.helpMenu

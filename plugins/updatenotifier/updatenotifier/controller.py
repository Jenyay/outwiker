#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from .i18n import get_
from .updatedialogcontroller import UpdateDialogController


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
        self._application = application


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        if self._application.mainWindow != None:
            self.__createMenu()


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        if self._application.mainWindow != None:
            self._application.mainWindow.Unbind (wx.EVT_MENU, id=self.UPDATE_ID, handler=self.__onCheckUpdate)
            self._helpMenu.Delete (self.UPDATE_ID)


    def __createMenu (self):
        """Добавление пункта меню для проверки обновлений"""
        assert self._application.mainWindow != None

        self._helpMenu.Append (id=self.UPDATE_ID, text=_(u"Check for Updates..."))
        self._application.mainWindow.Bind (wx.EVT_MENU, self.__onCheckUpdate, id=self.UPDATE_ID)


    def __onCheckUpdate (self, event):
        updateDialogController = UpdateDialogController (self._application)
        updateDialogController.ShowModal()


    @property
    def _helpMenu (self):
        return self._application.mainWindow.mainMenu.helpMenu

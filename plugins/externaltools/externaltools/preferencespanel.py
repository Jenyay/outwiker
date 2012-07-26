#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx


class PreferencesPanel (wx.Panel):
    """
    Панель с настройками
    """
    def __init__ (self, parent, config):
        """
        parent - родитель панели (должен быть wx.Treebook)
        config - настройки из plugin._application.config
        """
        wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)
        self._config = config

        from .i18n import _
        global _

        self.__controller = PrefController (self, config)


    def LoadState(self):
        self.__controller.loadState()


    def Save (self):
        self.__controller.save()


class PrefController (object):
    """
    Контроллер для управления панелью настроек
    """
    def __init__ (self, prefPanel, config):
        self._prefPanel = prefPanel
        self._config = config


    def loadState (self):
        pass


    def save (self):
        pass

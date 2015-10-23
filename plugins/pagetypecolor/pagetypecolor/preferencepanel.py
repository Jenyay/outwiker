# -*- coding: UTF-8 -*-

import wx

from i18n import get_
from config import PageTypeColorConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class PreferencePanel (BasePrefPanel):
    """
    Панель с настройками
    """
    def __init__ (self, parent, config):
        """
        parent - родитель панели (должен быть wx.Treebook)
        config - настройки из plugin._application.config
        """
        super (PreferencePanel, self).__init__ (parent)

        global _
        _ = get_()

        self.__createGui()
        self.__controller = PrefPanelController (self, config)


    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)


    def LoadState(self):
        self.__controller.loadState()


    def Save (self):
        self.__controller.save()



class PrefPanelController (object):
    """
    Контроллер для панели настроек
    """
    def __init__ (self, ownerPanel, config):
        self._panel = ownerPanel
        self._config = PageTypeColorConfig (config)


    def loadState (self):
        pass


    def save (self):
        pass

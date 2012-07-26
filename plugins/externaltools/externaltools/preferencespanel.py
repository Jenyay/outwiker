#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx

from .toolslistpanel import ToolsListPanel
from .i18n import get_
from .toolsconfig import ToolsConfig


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

        # from .i18n import _
        global _
        _ = get_()

        self.__makeGui()
        self.__controller = PrefController (self, config)


    def LoadState(self):
        self.__controller.loadState()


    def Save (self):
        self.__controller.save()


    def __makeGui (self):
        self.toolsLabel = wx.StaticText (self, -1, _(u"Tools List"))
        self.appendToolsButton = wx.Button (self, -1, _(u"Append Tools"))
        self.toolsList = ToolsListPanel (self)

        self.appendToolsButton.Bind (wx.EVT_BUTTON, self.__onAppendTools)
        self.__layout()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (0, 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (2)

        mainSizer.Add (self.toolsLabel, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        mainSizer.Add (self.appendToolsButton, 1, flag = wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add (self.toolsList, 1, flag = wx.EXPAND | wx.ALL, border=2)

        self.SetSizer (mainSizer)
        self.Layout()


    def __onAppendTools (self, event):
        self.toolsList.addTool()


class PrefController (object):
    """
    Контроллер для управления панелью настроек
    """
    def __init__ (self, prefPanel, config):
        self._prefPanel = prefPanel
        self._config = config


    def loadState (self):
        toolsConfig = ToolsConfig (self._config)
        self._prefPanel.toolsList.tools = toolsConfig.tools
        self._prefPanel.Layout()


    def save (self):
        pass

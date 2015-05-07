# -*- coding: utf-8 -*-

import ConfigParser

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.exceptions import PreferencesException

from .toolslistpanel import ToolsListPanel
from .i18n import get_
from .config import ExternalToolsConfig


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

        global _
        _ = get_()

        self.__makeGui()
        self.__controller = PrefController (self, config)


    def __makeGui (self):
        self.warningCheckBox = wx.CheckBox (
            self,
            -1,
            _(u'Show warning before executing applications by (:exec:) command')
        )

        self.toolsLabel = wx.StaticText (self, -1, _(u"Tools List"))
        self.appendToolsButton = wx.Button (self, -1, _(u"Append Tools"))
        self.toolsListPanel = ToolsListPanel (self)

        self.appendToolsButton.Bind (wx.EVT_BUTTON, self.__onAppendTools)
        self.__layout()


    def LoadState(self):
        self.__controller.loadState()


    def Save (self):
        self.__controller.save()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (3)

        mainSizer.Add (self.warningCheckBox, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        mainSizer.Add (self.toolsLabel, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        mainSizer.Add (self.appendToolsButton, 1, flag = wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add (self.toolsListPanel, 1, flag = wx.EXPAND | wx.ALL, border=2)

        self.SetSizer (mainSizer)
        self.Layout()


    def __onAppendTools (self, event):
        self.toolsListPanel.addTool()


class PrefController (object):
    """
    Контроллер для управления панелью настроек
    """
    def __init__ (self, prefPanel, config):
        self._prefPanel = prefPanel
        self._config = config


    def loadState (self):
        toolsConfig = ExternalToolsConfig (self._config)
        self._prefPanel.warningCheckBox.SetValue (toolsConfig.execWarning)
        self._prefPanel.toolsListPanel.tools = toolsConfig.tools
        self._prefPanel.Layout()


    def save (self):
        toolsConfig = ExternalToolsConfig (self._config)
        try:
            toolsConfig.tools = self._prefPanel.toolsListPanel.tools
            toolsConfig.execWarning = self._prefPanel.warningCheckBox.GetValue()
        except ConfigParser.Error:
            MessageBox (_(u"Can't save options"),
                        _(u"Error"),
                        wx.OK | wx.ICON_ERROR)
            raise PreferencesException()

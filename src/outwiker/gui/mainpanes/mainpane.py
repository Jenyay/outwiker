# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

import wx.aui


class MainPane(object, metaclass=ABCMeta):
    """
    Базовый класс для хранения основных панелей главного окна
    """

    def __init__(self, parent, auiManager, application):
        """
        parent - родитель панели
        application - экземпляр outwiker.core.application.ApplicationParams
        """
        self._parent = parent
        self._auiManager = auiManager
        self._application = application
        self._panel = self._createPanel()
        self._config = self._createConfig()

        pane = self._createPane()
        self._auiManager.AddPane(self._panel, pane)

    def _savePaneInfo(self, param, paneInfo):
        """
        Сохранить в конфиг информацию о dockable-панели (AuiPaneInfo)
        """
        string_info = self._auiManager.SavePaneInfo(paneInfo)
        param.value = string_info

    def _loadPaneInfo(self, param):
        """
        Загрузить из конфига и вернуть информацию о
        dockable-панели (AuiPaneInfo)
        """
        string_info = param.value

        if len(string_info) == 0:
            return

        pane = wx.aui.AuiPaneInfo()
        try:
            self._auiManager.LoadPaneInfo(string_info, pane)
        except Exception:
            return

        return pane

    def loadPaneSize(self):
        self.pane.BestSize((self.config.width.value,
                            self.config.height.value))

    def show(self):
        self.pane.Show()

    def hide(self):
        self.pane.Hide()

    def isShown(self):
        return self.pane.IsShown()

    def close(self):
        self.panel.Close()
        self._parent = None
        self._panel = None

    def saveParams(self):
        self._savePaneInfo(self.config.pane,
                           self._auiManager.GetPane(self.panel))

        self.config.width.value = self.panel.GetSize()[0]
        self.config.height.value = self.panel.GetSize()[1]

    def setFocus(self):
        self.panel.SetFocus()

    def setBackgroundColour(self, colour):
        self.panel.SetBackgroundColour(colour)

    def setForegroundColour(self, colour):
        self.panel.SetForegroundColour(colour)

    @abstractproperty
    def caption(self):
        pass

    @abstractmethod
    def _createPanel(self):
        pass

    @abstractmethod
    def _createConfig(self):
        pass

    @property
    def panel(self):
        return self._panel

    @property
    def config(self):
        return self._config

    @property
    def parent(self):
        return self._parent

    @property
    def application(self):
        return self._application

    @property
    def pane(self):
        return self._auiManager.GetPane(self.panel)

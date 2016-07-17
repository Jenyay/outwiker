# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

from outwiker.core.system import getImagesDir
import outwiker.core.commands
from .guiconfig import TrayConfig
from outwiker.actions.exit import ExitAction


def getTrayIconController(appliction, parentWnd):
    if os.name == "nt":
        return TrayIconControllerWindows(appliction, parentWnd)
    else:
        return TrayIconControllerLinux(appliction, parentWnd)


class TrayIconControllerBase(wx.EvtHandler):
    __metaclass__ = ABCMeta

    def __init__(self, application, mainWnd):
        super(TrayIconControllerBase, self).__init__()
        self.mainWnd = mainWnd
        self._application = application
        self.config = TrayConfig(self._application.config)

        self._trayIcon = None

    @abstractmethod
    def _createTrayIcon(self):
        pass

    def initialize(self):
        self._trayIcon = self._createTrayIcon()
        self._bind()

    def destroy(self):
        self._trayIcon.removeTrayIcon()
        self._unbind()
        self._trayIcon.Destroy()

    def restoreWindow(self):
        self.mainWnd.Show()
        self.mainWnd.Iconize(False)
        if not self.config.alwaysShowTrayIcon.value:
            self._trayIcon.removeTrayIcon()
        self.mainWnd.Raise()
        self.mainWnd.SetFocus()

    def _bind(self):
        self.mainWnd.Bind(wx.EVT_ICONIZE, self.__onIconize)
        self.mainWnd.Bind(wx.EVT_IDLE, self.__onIdle)

        self._application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        self._application.onPageSelect += self.__OnTaskBarUpdate
        self._application.onTreeUpdate += self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate += self.__OnTaskBarUpdate

    def _unbind(self):
        self.mainWnd.Unbind(wx.EVT_ICONIZE, handler = self.__onIconize)
        self.mainWnd.Unbind(wx.EVT_IDLE, handler=self.__onIdle)

        self._application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        self._application.onPageSelect -= self.__OnTaskBarUpdate
        self._application.onTreeUpdate -= self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate -= self.__OnTaskBarUpdate

    def updateTrayIcon(self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if(self.config.alwaysShowTrayIcon.value or
               (self.config.minimizeToTray.value and self.mainWnd.IsIconized())):
            self._trayIcon.showTrayIcon()
        else:
            self._trayIcon.removeTrayIcon()

    def __OnTaskBarUpdate(self, page):
        self.updateTrayIcon()

    def __onIdle(self, event):
        self.__initMainWnd()
        self.updateTrayIcon()
        self.mainWnd.Unbind(wx.EVT_IDLE, handler=self.__onIdle)

    def __onPreferencesDialogClose(self, prefDialog):
        self.updateTrayIcon()

    def __initMainWnd(self):
        if self.config.startIconized.value:
            self.mainWnd.Iconize(True)
        else:
            self.mainWnd.Show()

    def __onIconize(self, event):
        if event.IsIconized():
            # Окно свернули
            self.__iconizeWindow()
        else:
            self.restoreWindow()

        self.updateTrayIcon()

    def __iconizeWindow(self):
        """
        Свернуть окно
        """
        if self.config.minimizeToTray.value:
            # В трей добавим иконку, а окно спрячем
            self._trayIcon.showTrayIcon()
            self.mainWnd.Show()
            self.mainWnd.Hide()


class TrayIconControllerWindows(TrayIconControllerBase):
    def _createTrayIcon(self):
        return TrayIconWindows(self._application, self.mainWnd)

    def _bind(self):
        super(TrayIconControllerWindows, self)._bind()
        self._trayIcon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.__OnTrayLeftClick)

        self.Bind(wx.EVT_MENU, self.__onExit, id=self._trayIcon.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.__onRestore, id=self._trayIcon.ID_RESTORE)

    def _unbind(self):
        super(TrayIconControllerWindows, self)._unbind()
        self._trayIcon.Unbind(wx.EVT_TASKBAR_LEFT_DOWN, handler = self.__OnTrayLeftClick)

        self.Unbind(wx.EVT_MENU, handler = self.__onExit, id=self._trayIcon.ID_EXIT)
        self.Unbind(wx.EVT_MENU, handler = self.__onRestore, id=self._trayIcon.ID_RESTORE)

    def __onRestore(self, event):
        self.restoreWindow()

    def __OnTrayLeftClick(self, event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()

    def __onExit(self, event):
        self._application.actionController.getAction(ExitAction.stringId).run(None)


class TrayIconWindows(wx.TaskBarIcon):
    def __init__(self, application, mainWnd):
        super(TrayIconWindows, self).__init__()
        self._application = application
        self.mainWnd = mainWnd

        self.ID_RESTORE = wx.NewId()
        self.ID_EXIT = wx.NewId()
        self.icon = wx.Icon(os.path.join(getImagesDir(), "outwiker.ico"),
                            wx.BITMAP_TYPE_ANY)

    def CreatePopupMenu(self):
        trayMenu = wx.Menu()
        trayMenu.Append(self.ID_RESTORE, _(u"Restore"))
        trayMenu.Append(self.ID_EXIT, _(u"Exit"))
        return trayMenu

    def showTrayIcon(self):
        tooltip = outwiker.core.commands.getMainWindowTitle(self._application)
        self.SetIcon(self.icon, tooltip)

    def removeTrayIcon(self):
        if self.IsIconInstalled():
            self.RemoveIcon()


class TrayIconControllerLinux(object):
    def __init__(self, mainWnd):
        pass


    def initialize(self):
        pass


    def Destroy(self):
        pass

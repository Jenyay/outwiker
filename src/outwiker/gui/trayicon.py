# -*- coding: utf-8 -*-

import os
import logging

import wx
import wx.adv

from outwiker.actions.exit import ExitAction
from outwiker.api.gui.mainwindow import getMainWindowTitle
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.guiconfig import TrayConfig


logger = logging.getLogger('outwiker.gui.trayicon')


def getTrayIconController(application, parentWnd) -> 'TrayIconController':
    if os.name == "nt":
        fname = 'outwiker_16x16.png'
    else:
        fname = 'outwiker_64x64.png'

    return TrayIconController(application,
                              parentWnd,
                              getBuiltinImagePath(fname))


class TrayIconController(wx.EvtHandler):
    def __init__(self, application, mainWnd, iconFileName):
        super(TrayIconController, self).__init__()
        self.mainWnd = mainWnd
        self._application = application
        self._iconFileName = iconFileName
        self.config = TrayConfig(self._application.config)
        self._trayIcon = TrayIcon(self._application, self.mainWnd, self._iconFileName)
        self._bind()

    def destroy(self):
        self._trayIcon.removeTrayIcon()
        self._unbind()
        self._trayIcon.Destroy()
        self._application = None
        self._trayIcon = None

    def showTrayIcon(self):
        self._trayIcon.showTrayIcon()

    def removeTrayIcon(self):
        self._trayIcon.removeTrayIcon()

    def hideToTray(self):
        self.mainWnd.hideToTray()

    def restoreWindow(self):
        if not self.config.alwaysShowTrayIcon.value:
            self._trayIcon.removeTrayIcon()

        self.mainWnd.Iconize(False)
        self.mainWnd.Raise()

        if not self.mainWnd.IsShown():
            self.mainWnd.Show()

        self.mainWnd.SetFocus()

    def _bind(self):
        self._trayIcon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN,
                            self._onTrayLeftClick)

        self._trayIcon.Bind(wx.EVT_MENU, self._onPopupMenu)

        self._application.onPreferencesDialogClose += self._onPreferencesDialogClose
        self._application.onPageSelect += self._onTaskBarUpdate
        self._application.onTreeUpdate += self._onTaskBarUpdate
        self._application.onEndTreeUpdate += self._onTaskBarUpdate

    def _unbind(self):
        self._trayIcon.Unbind(wx.adv.EVT_TASKBAR_LEFT_DOWN,
                              handler=self._onTrayLeftClick)

        self._trayIcon.Unbind(wx.EVT_MENU, handler=self._onPopupMenu)

        self._application.onPreferencesDialogClose -= self._onPreferencesDialogClose
        self._application.onPageSelect -= self._onTaskBarUpdate
        self._application.onTreeUpdate -= self._onTaskBarUpdate
        self._application.onEndTreeUpdate -= self._onTaskBarUpdate

    def updateTrayIcon(self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if self.config.alwaysShowTrayIcon.value or not self.mainWnd.IsShown():
            self.showTrayIcon()
        else:
            self.removeTrayIcon()

    def _onPreferencesDialogClose(self, _prefDialog):
        self.updateTrayIcon()

    def _onTaskBarUpdate(self, _page):
        self.updateTrayIcon()

    def _onTrayLeftClick(self, _event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()

    def _onPopupMenu(self, event):
        if event.GetId() == self._trayIcon.ID_RESTORE:
            self.restoreWindow()
        elif event.GetId() == self._trayIcon.ID_EXIT:
            self._application.actionController.getAction(ExitAction.stringId).run(None)


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, application, mainWnd, iconFileName):
        super().__init__()
        self._application = application
        self.mainWnd = mainWnd
        self._iconFileName = iconFileName

        logger.debug('Tray icon available: {}'.format(self.IsAvailable()))

        self.ID_RESTORE = None
        self.ID_EXIT = None
        self.icon = wx.Icon(self._iconFileName, wx.BITMAP_TYPE_ANY)

    def CreatePopupMenu(self):
        trayMenu = wx.Menu()
        self.ID_RESTORE = trayMenu.Append(wx.ID_ANY, _("Restore")).GetId()
        self.ID_EXIT = trayMenu.Append(wx.ID_ANY, _("Exit")).GetId()
        return trayMenu

    def update(self):
        if self.IsIconInstalled():
            tooltip = getMainWindowTitle(self._application)
            self.SetIcon(self.icon, tooltip)

    def showTrayIcon(self):
        if not self.IsIconInstalled():
            tooltip = getMainWindowTitle(self._application)
            self.SetIcon(self.icon, tooltip)

    def removeTrayIcon(self):
        if self.IsIconInstalled():
            self.RemoveIcon()

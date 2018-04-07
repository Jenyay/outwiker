# -*- coding: utf-8 -*-

import os
import logging

import wx
import wx.adv

import outwiker.core.commands
from outwiker.actions.exit import ExitAction
from outwiker.core.system import getImagesDir
from outwiker.gui.guiconfig import TrayConfig


logger = logging.getLogger('outwiker.gui.trayicon')


def getTrayIconController(application, parentWnd):
    if os.name == "nt":
        fname = 'outwiker_16x16.png'
    else:
        fname = 'outwiker_64x64.png'

    return TrayIconController(application,
                              parentWnd,
                              os.path.join(getImagesDir(), fname))


class TrayIconController(wx.EvtHandler):
    def __init__(self, application, mainWnd, iconFileName):
        super(TrayIconController, self).__init__()
        self.mainWnd = mainWnd
        self._application = application
        self._iconFileName = iconFileName
        self.config = TrayConfig(self._application.config)
        self._trayIcon = self._createTrayIcon()
        self._bind()

    def _createTrayIcon(self):
        return TrayIcon(self._application, self.mainWnd, self._iconFileName)

    def destroy(self):
        self._trayIcon.removeTrayIcon()
        self._unbind()
        self._trayIcon.Destroy()
        self._mainWindow = None
        self._application = None
        self._trayIcon = None

    def restoreWindow(self):
        if not self.config.alwaysShowTrayIcon.value:
            self._trayIcon.removeTrayIcon()

        self.mainWnd.Iconize(False)
        self.mainWnd.Raise()

        if not self.mainWnd.IsShown():
            self.mainWnd.Show()

        self.mainWnd.SetFocus()

    def _bind(self):
        self.mainWnd.Bind(wx.EVT_ICONIZE, self.__onIconize)

        self._trayIcon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN,
                            self.__OnTrayLeftClick)

        self._trayIcon.Bind(wx.EVT_MENU, self.__onPopupMenu)

        self._application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        self._application.onPageSelect += self.__OnTaskBarUpdate
        self._application.onTreeUpdate += self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate += self.__OnTaskBarUpdate

    def _unbind(self):
        self.mainWnd.Unbind(wx.EVT_ICONIZE, handler=self.__onIconize)

        self._trayIcon.Unbind(wx.adv.EVT_TASKBAR_LEFT_DOWN,
                              handler=self.__OnTrayLeftClick)

        self._trayIcon.Unbind(wx.EVT_MENU, handler=self.__onPopupMenu)

        self._application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        self._application.onPageSelect -= self.__OnTaskBarUpdate
        self._application.onTreeUpdate -= self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate -= self.__OnTaskBarUpdate

    def updateTrayIcon(self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if (self.config.alwaysShowTrayIcon.value or
                (self.config.minimizeToTray.value and
                 (self.mainWnd.IsIconized() or
                  not self.mainWnd.IsShown()))):
            self._trayIcon.showTrayIcon()
        else:
            self._trayIcon.removeTrayIcon()

    def __onPreferencesDialogClose(self, prefDialog):
        self.updateTrayIcon()

    def __onIconize(self, event):
        if event.IsIconized() and self.config.minimizeToTray.value:
            # Окно свернули
            self.mainWnd.Hide()
        self.updateTrayIcon()

    def __OnTaskBarUpdate(self, page):
        self.updateTrayIcon()

    def __OnTrayLeftClick(self, event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()

    def __onPopupMenu(self, event):
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

        logger.debug(u'Tray icon available: {}'.format(self.IsAvailable()))

        self.ID_RESTORE = None
        self.ID_EXIT = None
        self.icon = wx.Icon(self._iconFileName, wx.BITMAP_TYPE_ANY)

    def CreatePopupMenu(self):
        trayMenu = wx.Menu()
        self.ID_RESTORE = trayMenu.Append(wx.ID_ANY, _(u"Restore")).GetId()
        self.ID_EXIT = trayMenu.Append(wx.ID_ANY, _(u"Exit")).GetId()
        return trayMenu

    def showTrayIcon(self):
        tooltip = outwiker.core.commands.getMainWindowTitle(self._application)
        self.SetIcon(self.icon, tooltip)

    def removeTrayIcon(self):
        if self.IsIconInstalled():
            self.RemoveIcon()

# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx
import wx.adv

import outwiker.core.commands
from outwiker.actions.exit import ExitAction
from outwiker.core.system import getImagesDir
from outwiker.core.defines import APP_DATA_DISABLE_MINIMIZING
from outwiker.gui.guiconfig import TrayConfig


def getTrayIconController(application, parentWnd):
    if os.name == "nt":
        return TrayIconControllerWindows(application, parentWnd)
    else:
        return TrayIconControllerLinux(application, parentWnd)


class TrayIconControllerBase(wx.EvtHandler):
    #__metaclass__ = ABCMeta

    def __init__(self, application, mainWnd):
        super(TrayIconControllerBase, self).__init__()
        self.mainWnd = mainWnd
        self._application = application
        self.config = TrayConfig(self._application.config)

        self._trayIcon = None

    #@abstractmethod
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
        if not self.config.alwaysShowTrayIcon.value:
            self._trayIcon.removeTrayIcon()
        self.mainWnd.Iconize(False)
        self.mainWnd.Show()
        self.mainWnd.Raise()
        self.mainWnd.SetFocus()

    def _bind(self):
        self.mainWnd.Bind(wx.EVT_ICONIZE, self.__onIconize)
        self.mainWnd.Bind(wx.EVT_IDLE, self.__onIdle)

        self._application.onPreferencesDialogClose += self.__onPreferencesDialogClose

    def _unbind(self):
        self.mainWnd.Unbind(wx.EVT_ICONIZE, handler=self.__onIconize)
        self.mainWnd.Unbind(wx.EVT_IDLE, handler=self.__onIdle)

        self._application.onPreferencesDialogClose -= self.__onPreferencesDialogClose

    def updateTrayIcon(self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if(self.config.alwaysShowTrayIcon.value or
               (self.config.minimizeToTray.value and (self.mainWnd.IsIconized() or not self.mainWnd.IsShown()))):
            self._trayIcon.showTrayIcon()
        else:
            self._trayIcon.removeTrayIcon()

    def __onIdle(self, event):
        self.mainWnd.Unbind(wx.EVT_IDLE, handler=self.__onIdle)
        if (self.config.startIconized.value and not
                self._application.sharedData.get(APP_DATA_DISABLE_MINIMIZING, False)):
            self.mainWnd.Iconize(True)
        else:
            self.mainWnd.Show()
            self.updateTrayIcon()

    def __onPreferencesDialogClose(self, prefDialog):
        self.updateTrayIcon()

    def __onIconize(self, event):
        if event.IsIconized() and self.config.minimizeToTray.value:
            # Окно свернули
            self.mainWnd.Hide()
        self.updateTrayIcon()


class TrayIconControllerWindows(TrayIconControllerBase):
    def _createTrayIcon(self):
        return TrayIconWindows(self._application, self.mainWnd)

    def _bind(self):
        super(TrayIconControllerWindows, self)._bind()

        #TODO: wx.EVT_TASKBAR_LEFT_DOWN is absent on windows 10 (64x)
        #self._trayIcon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.__OnTrayLeftClick)
        self._trayIcon.Bind(wx.EVT_MENU, self.__onExit, id=self._trayIcon.ID_EXIT)
        self._trayIcon.Bind(wx.EVT_MENU, self.__onRestore, id=self._trayIcon.ID_RESTORE)

        self._application.onPageSelect += self.__OnTaskBarUpdate
        self._application.onTreeUpdate += self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate += self.__OnTaskBarUpdate

    def _unbind(self):
        super(TrayIconControllerWindows, self)._unbind()

        # TODO: wx.EVT_TASKBAR_LEFT_DOWN is absent on windows 10 (64x)
        self._trayIcon.Unbind(wx.EVT_TASKBAR_LEFT_DOWN,
                              handler=self.__OnTrayLeftClick)

        self._trayIcon.Unbind(wx.EVT_MENU,
                              handler=self.__onExit,
                              id=self._trayIcon.ID_EXIT)
        self._trayIcon.Unbind(wx.EVT_MENU,
                              handler=self.__onRestore,
                              id=self._trayIcon.ID_RESTORE)

        self._application.onPageSelect -= self.__OnTaskBarUpdate
        self._application.onTreeUpdate -= self.__OnTaskBarUpdate
        self._application.onEndTreeUpdate -= self.__OnTaskBarUpdate

    def __OnTaskBarUpdate(self, page):
        self.updateTrayIcon()

    def __onRestore(self, event):
        self.restoreWindow()

    def __OnTrayLeftClick(self, event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()

    def __onExit(self, event):
        self._application.actionController.getAction(ExitAction.stringId).run(None)


class TrayIconControllerLinux(TrayIconControllerBase):
    def _createTrayIcon(self):
        return TrayIconLinux(self._application, self.mainWnd)

    def _bind(self):
        super(TrayIconControllerLinux, self)._bind()

        self._restoreHandlerId = self._trayIcon.restoreMenuItem.connect(
            'activate', self.__onRestore)

        self._exitHandlerId = self._trayIcon.exitMenuItem.connect(
            'activate', self.__onExit)

    def _unbind(self):
        super(TrayIconControllerLinux, self)._unbind()
        self._trayIcon.restoreMenuItem.disconnect(self._restoreHandlerId)
        self._trayIcon.exitMenuItem.disconnect(self._exitHandlerId)

    def __onRestore(self, obj):
        self.restoreWindow()

    def __onExit(self, obj):
        self._application.actionController.getAction(ExitAction.stringId).run(None)

class TrayIconWindows(wx.adv.TaskBarIcon):
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


class TrayIconLinux(object):
    def __init__(self, application, mainWnd):
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('AppIndicator3', '0.1')

        from gi.repository import Gtk as gtk
        from gi.repository import AppIndicator3

        self._application = application
        self._mainWnd = mainWnd

        self._icon = os.path.abspath(os.path.join(getImagesDir(),
                                                  "outwiker_64x64.png"))
        assert os.path.exists(self._icon)
        self._indicator = AppIndicator3.Indicator.new("OutWiker",
                                                 self._icon,
                                                  AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        menu = gtk.Menu()
        self.restoreMenuItem = gtk.MenuItem(_('Restore'))
        self.restoreMenuItem.show()

        self.exitMenuItem = gtk.MenuItem(_('Exit'))
        self.exitMenuItem.show()

        menu.append(self.restoreMenuItem)
        menu.append(self.exitMenuItem)
        self._indicator.set_menu(menu)

    def showTrayIcon(self):
        from gi.repository import AppIndicator3
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def removeTrayIcon(self):
        from gi.repository import AppIndicator3
        self._indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

    def Destroy(self):
        # self.removeTrayIcon()
        self._indicator = None

# -*- coding: utf-8 -*-

import os

import wx

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from .guiconfig import TrayConfig
from outwiker.actions.exit import ExitAction


class OutwikerTrayIcon (wx.TaskBarIcon):
    """
    Класс для работы с иконкой в трее
    """
    def __init__ (self, mainWnd):
        wx.TaskBarIcon.__init__ (self)
        self.mainWnd = mainWnd
        self.config = TrayConfig (Application.config)

        self.ID_RESTORE = wx.NewId()
        self.ID_EXIT = wx.NewId()

        self.icon = wx.Icon(os.path.join (outwiker.core.system.getImagesDir(), "outwiker.ico"), wx.BITMAP_TYPE_ANY)

        self.__bind()


    def updateTrayIcon (self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if (self.config.alwaysShowTrayIcon.value or
                (self.config.minimizeToTray.value and self.mainWnd.IsIconized())):
            self.ShowTrayIcon()
        else:
            self.removeTrayIcon()


    def __bind (self):
        self.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.__OnTrayLeftClick)
        self.mainWnd.Bind (wx.EVT_ICONIZE, self.__onIconize)
        self.mainWnd.Bind (wx.EVT_IDLE, self.__onIdle)

        self.Bind(wx.EVT_MENU, self.__onExit, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.__onRestore, id=self.ID_RESTORE)

        Application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        Application.onPageSelect += self.__OnTaskBarUpdate
        Application.onTreeUpdate += self.__OnTaskBarUpdate
        Application.onEndTreeUpdate += self.__OnTaskBarUpdate


    def __unbind (self):
        self.Unbind (wx.EVT_TASKBAR_LEFT_DOWN, handler = self.__OnTrayLeftClick)
        self.mainWnd.Unbind (wx.EVT_ICONIZE, handler = self.__onIconize)

        self.Unbind(wx.EVT_MENU, handler = self.__onExit, id=self.ID_EXIT)
        self.Unbind(wx.EVT_MENU, handler = self.__onRestore, id=self.ID_RESTORE)

        Application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        Application.onPageSelect -= self.__OnTaskBarUpdate
        Application.onTreeUpdate -= self.__OnTaskBarUpdate
        Application.onEndTreeUpdate -= self.__OnTaskBarUpdate


    def __OnTaskBarUpdate (self, page):
        self.updateTrayIcon()


    def __onIdle (self, event):
        self.__initMainWnd()
        self.updateTrayIcon()
        self.mainWnd.Unbind (wx.EVT_IDLE, handler=self.__onIdle)


    def __onPreferencesDialogClose (self, prefDialog):
        self.updateTrayIcon()


    def __initMainWnd (self):
        if self.config.startIconized.value:
            self.mainWnd.Iconize (True)
        else:
            self.mainWnd.Show()


    def __onIconize (self, event):
        if event.Iconized():
            # Окно свернули
            self.__iconizeWindow ()
        else:
            self.restoreWindow()

        self.updateTrayIcon()


    def __iconizeWindow (self):
        """
        Свернуть окно
        """
        if self.config.minimizeToTray.value:
            # В трей добавим иконку, а окно спрячем
            self.ShowTrayIcon()
            self.mainWnd.Hide()


    def removeTrayIcon (self):
        """
        Удалить иконку из трея
        """
        if self.IsIconInstalled():
            self.RemoveIcon()


    def __onRestore (self, event):
        self.restoreWindow()


    def __OnTrayLeftClick (self, event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()


    def restoreWindow (self):
        self.mainWnd.Show ()
        self.mainWnd.Iconize (False)
        if not self.config.alwaysShowTrayIcon.value:
            self.removeTrayIcon()
        self.mainWnd.Raise()
        self.mainWnd.SetFocus()


    def __onExit (self, event):
        Application.actionController.getAction (ExitAction.stringId).run(None)


    def CreatePopupMenu (self):
        trayMenu = wx.Menu()
        trayMenu.Append (self.ID_RESTORE, _(u"Restore"))
        trayMenu.Append (self.ID_EXIT, _(u"Exit"))

        Application.onTrayPopupMenu (trayMenu, self)

        return trayMenu


    def Destroy (self):
        self.removeTrayIcon()
        self.__unbind()
        super (OutwikerTrayIcon, self).Destroy()


    def ShowTrayIcon (self):
        tooltip = outwiker.core.commands.getMainWindowTitle (Application)
        self.SetIcon(self.icon, tooltip)

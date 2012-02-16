#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.application import Application
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import TrayConfig
from .basemainwnd import BaseMainWndTest


class TrayNormalTest(BaseMainWndTest):
    """
    Тесты на сворачиваемость главного окна в трей. Нормальный запуск окна (не свернутый в трей)
    """
    def testTrayInterface (self):
        self.assertEqual (self.wnd, self.wnd.taskBarIcon.mainWnd)
        self.assertNotEqual (None, self.wnd.taskBarIcon.config)


    def testTrayNormalConfig (self):
        self.wnd.taskBarIcon.config.minimizeToTray.remove_option()
        self.wnd.taskBarIcon.config.startIconized.remove_option()
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.remove_option()

        self.assertTrue (self.wnd.taskBarIcon.config.minimizeToTray.value)
        self.assertFalse (self.wnd.taskBarIcon.config.startIconized.value)
        self.assertFalse (self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value)


    def testTrayMinimize1 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = True
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = False
        self.wnd.taskBarIcon.config.startIconized.value = False
        Application.onPreferencesDialogClose(None)
        #self._processEvents()

        self.wnd.Iconize(True)
        self._processEvents()

        self.assertFalse (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())


    def testTrayMinimize2 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = False
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = False
        self.wnd.taskBarIcon.config.startIconized.value = False
        Application.onPreferencesDialogClose(None)
        #self._processEvents()

        self.wnd.Iconize(True)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())


    def testTrayMinimize3 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = True
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = True
        self.wnd.taskBarIcon.config.startIconized.value = False

        Application.onPreferencesDialogClose(None)
        #self._processEvents()

        self.wnd.Show()
        self.wnd.Iconize(False)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.Iconize(True)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())


    def testTrayMinimize4 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = False
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = True
        self.wnd.taskBarIcon.config.startIconized.value = False

        Application.onPreferencesDialogClose(None)
        #self._processEvents()

        self.wnd.Show()
        self.wnd.Iconize(False)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.Iconize(True)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())



class TrayIconizedTest (BaseMainWndTest):
    def setUp (self):
        config = TrayConfig (Application.config)
        config.startIconized.value = True

        BaseMainWndTest.setUp (self)


    def testStartMinimize1 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = True
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = False
    
        Application.onPreferencesDialogClose(None)
        self._processEvents()

        self.assertTrue (self.wnd.IsIconized())
        self.assertFalse (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())


    def testStartMinimize2 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = True
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = True
    
        Application.onPreferencesDialogClose(None)
        self._processEvents()

        self.assertFalse (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())


    def testStartMinimize3 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = False
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = True
    
        Application.onPreferencesDialogClose(None)
        self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())


    def testStartMinimize4 (self):
        self.wnd.taskBarIcon.config.minimizeToTray.value = False
        self.wnd.taskBarIcon.config.alwaysShowTrayIcon.value = False
    
        Application.onPreferencesDialogClose(None)
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())

        self.wnd.taskBarIcon.restoreWindow()
        #self._processEvents()

        self.assertTrue (self.wnd.IsShown())
        self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())

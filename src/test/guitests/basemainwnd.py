# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.application import Application
from outwiker.core.commands import registerActions
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import GeneralGuiConfig, MainWindowConfig
from outwiker.gui.actioncontroller import ActionController


class BaseMainWndTest(unittest.TestCase):
    def _processEvents (self):
        """
        Обработать накопившиеся сообщения
        """
        count = 0

        app = wx.GetApp()

        while app.Pending():
            count += 1
            app.Dispatch()

        return count


    def setUp(self):
        Application.config.remove_section (MainWindowConfig.MAIN_WINDOW_SECTION)

        generalConfig = GeneralGuiConfig (Application.config)
        generalConfig.askBeforeExit.value = False

        self.wnd = MainWindow (None, -1, "")
        Application.mainWindow = self.wnd
        Application.actionController = ActionController (self.wnd, Application.config)
        wx.GetApp().SetTopWindow (self.wnd)

        registerActions (Application)
        self.wnd.createGui()


    def tearDown (self):
        wx.GetApp().Yield()
        self.wnd.Close()
        self.wnd.Hide()
        self._processEvents()
        Application.mainWindow = None

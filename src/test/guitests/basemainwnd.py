#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.application import Application
from outwiker.core.commands import registerActions
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import GeneralGuiConfig, MainWindowConfig
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.actioncontroller import ActionController

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction


class BaseMainWndTest(unittest.TestCase):
    def _processEvents (self):
        """
        Обработать накопившиеся сообщения
        """
        count = 0

        loop = wx.EventLoop.GetActive()
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
        self.wnd.Close()
        self.wnd.Hide()
        self._processEvents()

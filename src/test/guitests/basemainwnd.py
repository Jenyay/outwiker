#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.application import Application
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.pages.html.htmlpage import HtmlPageFactory


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
        generalConfig = GeneralGuiConfig (Application.config)
        generalConfig.askBeforeExit.value = False

        self.wnd = MainWindow (None, -1, "")
        Application.mainWindow = self.wnd
        wx.GetApp().SetTopWindow (self.wnd)

        # Зарегистрировать действия для всех типов страниц
        HtmlPageFactory.registerActions (Application)


    def tearDown (self):
        self.wnd.Close()
        self.wnd.Hide()
        self._processEvents()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from core.application import Application
from gui.MainWindow import MainWindow
from gui.guiconfig import GeneralGuiConfig

from .basemainwnd import BaseMainWndTest

class MainWndTest(BaseMainWndTest):
	def testProperties (self):
		self.assertNotEqual (None, self.wnd.tree)
		self.assertNotEqual (None, self.wnd.pagePanel)
		self.assertNotEqual (None, self.wnd.attachPanel)
		self.assertNotEqual (None, self.wnd.mainMenu)
		self.assertNotEqual (None, self.wnd.mainToolbar)
		self.assertNotEqual (None, self.wnd.statusbar)
		self.assertNotEqual (None, self.wnd.taskBarIcon)

		self.assertNotEqual (None, self.wnd.mainWindowConfig)
		self.assertNotEqual (None, self.wnd.treeConfig)
		self.assertNotEqual (None, self.wnd.attachConfig)
		self.assertNotEqual (None, self.wnd.generalConfig)


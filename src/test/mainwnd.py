#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import gc

from core.application import Application
from gui.MainWindow import MainWindow
from gui.guiconfig import GeneralGuiConfig


class MainWndTest(unittest.TestCase):
	def setUp(self):
		generalConfig = GeneralGuiConfig (Application.config)
		generalConfig.askBeforeExitOption.value = False


	def test1 (self):
		wnd = MainWindow (None, -1, "")
		wnd.Update()

		self.assertNotEqual (None, wnd)

		wnd.Hide()
		wnd.Update()
		wnd.Close()

		#gc.collect()
		#print gc.get_referrers (wnd)

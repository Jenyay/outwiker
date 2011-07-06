#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import gc

import wx

from core.application import Application
from gui.MainWindow import MainWindow
from gui.guiconfig import GeneralGuiConfig


class MainWndTest(unittest.TestCase):
	def _processEvents (self):
		"""
		Обработать накопившиеся сообщения
		"""
		while self.eventloop.Pending():
			self.eventloop.Dispatch()


	def setUp(self):
		generalConfig = GeneralGuiConfig (Application.config)
		generalConfig.askBeforeExitOption.value = False

		self.wnd = MainWindow (None, -1, "")

		self.oldloop = wx.EventLoop.GetActive()
		self.eventloop = wx.EventLoop()
		wx.EventLoop.SetActive(self.eventloop)


	def tearDown (self):
		self.wnd.Close()
		self.wnd.Hide()
		self._processEvents()

		# Вызовем обработчик простоя, чтобы удалилось окно self.wnd
		#wx.GetApp().ProcessIdle()
		wx.EventLoop.SetActive(self.oldloop)


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


	def testTrayInterface (self):
		self.assertEqual (self.wnd, self.wnd.taskBarIcon.mainWnd)
		self.assertNotEqual (None, self.wnd.taskBarIcon.config)


	def testTrayNormalConfig (self):
		self.wnd.taskBarIcon.config.minimizeOption.remove_option()
		self.wnd.taskBarIcon.config.startIconizedOption.remove_option()
		self.wnd.taskBarIcon.config.alwaysShowTrayIconOption.remove_option()

		self.assertTrue (self.wnd.taskBarIcon.config.minimizeOption.value)
		self.assertFalse (self.wnd.taskBarIcon.config.startIconizedOption.value)
		self.assertFalse (self.wnd.taskBarIcon.config.alwaysShowTrayIconOption.value)


	def testTrayMinimize1 (self):
		self.wnd.taskBarIcon.config.minimizeOption.value = True
		self.wnd.taskBarIcon.config.startIconizedOption.value = False
		self.wnd.taskBarIcon.config.alwaysShowTrayIconOption.value = False

		self.wnd.Iconize(True)
		self._processEvents()

		self.assertTrue (self.wnd.IsIconized())
		self.assertFalse (self.wnd.IsShown())
		self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())


	def testTrayMinimize2 (self):
		self.wnd.taskBarIcon.config.minimizeOption.value = False
		self.wnd.taskBarIcon.config.startIconizedOption.value = False
		self.wnd.taskBarIcon.config.alwaysShowTrayIconOption.value = False

		self.wnd.Iconize(True)
		self._processEvents()

		self.assertTrue (self.wnd.IsIconized())
		self.assertTrue (self.wnd.IsShown())
		self.assertFalse (self.wnd.taskBarIcon.IsIconInstalled())


	def testTrayMinimize3 (self):
		self.wnd.taskBarIcon.config.minimizeOption.value = True
		self.wnd.taskBarIcon.config.startIconizedOption.value = False
		self.wnd.taskBarIcon.config.alwaysShowTrayIconOption.value = True

		Application.onMainWindowConfigChange()

		self.wnd.Show()
		self.wnd.Iconize(False)
		self._processEvents()

		self.assertFalse (self.wnd.IsIconized())
		self.assertTrue (self.wnd.IsShown())
		self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

		self.wnd.Iconize(True)
		self._processEvents()

		self.assertFalse (self.wnd.IsIconized())
		self.assertTrue (self.wnd.IsShown())
		self.assertTrue (self.wnd.taskBarIcon.IsIconInstalled())

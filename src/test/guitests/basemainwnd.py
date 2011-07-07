#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from core.application import Application
from gui.MainWindow import MainWindow
from gui.guiconfig import GeneralGuiConfig


class BaseMainWndTest(unittest.TestCase):
	def _processEvents (self):
		"""
		Обработать накопившиеся сообщения
		"""
		count = 0
		while self.eventloop.Pending():
			count += 1
			self.eventloop.Dispatch()

		return count


	def setUp(self):
		generalConfig = GeneralGuiConfig (Application.config)
		generalConfig.askBeforeExitOption.value = False

		self.wnd = MainWindow (None, -1, "")
		#wx.GetApp().SetTopWindow (self.wnd)

		self.oldloop = wx.EventLoop.GetActive()
		self.eventloop = wx.EventLoop()
		wx.EventLoop.SetActive(self.eventloop)

		#self._processEvents()


	def tearDown (self):
		self.wnd.Close()
		self.wnd.Hide()
		self._processEvents()

		# Вызовем обработчик простоя, чтобы удалилось окно self.wnd
		#wx.GetApp().ProcessIdle()
		wx.EventLoop.SetActive(self.oldloop)

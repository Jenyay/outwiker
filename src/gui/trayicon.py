#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import wx

import core.system
from core.application import Application


class OutwikerTrayIcon (wx.TaskBarIcon):
	"""
	Класс для работы с иконкой в трее
	"""
	def __init__ (self, mainWnd):
		wx.TaskBarIcon.__init__ (self)
		self.mainWnd = mainWnd

		self.ID_RESTORE = wx.NewId()
		self.ID_EXIT = wx.NewId()

		self.icon = wx.EmptyIcon()
		self.icon.CopyFromBitmap(wx.Bitmap(os.path.join (core.system.getImagesDir(), "outwiker_16.png"), wx.BITMAP_TYPE_ANY))

		self.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.OnTrayLeftClick)
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onRestore, id=self.ID_RESTORE)
		self.mainWnd.Bind (wx.EVT_ICONIZE, self.onIconize)

		self.initMainWnd()


	def initMainWnd (self):
		if Application.config.startIconizedOption.value:
			self.__iconizeWindow()
		else:
			self.mainWnd.Show()
	

	def onIconize (self, event):
		if self.mainWnd.IsIconized():
			# Окно свернули
			self.__iconizeWindow ()
	

	def __iconizeWindow (self):
		"""
		Свернуть окно
		"""
		if Application.config.minimizeOption.value:
			# В трей добавим иконку, а окно спрячем
			self.ShowIcon()
			self.mainWnd.Hide()
	

	def removeTrayIcon (self):
		"""
		Удалить иконку из трея
		"""
		if self.IsIconInstalled():
			self.RemoveIcon()


	def onRestore (self, event):
		self.__restoreMainWindow()


	def OnTrayLeftClick (self, event):
		self.__restoreMainWindow()
	

	def __restoreMainWindow (self):
		self.mainWnd.Show ()
		self.mainWnd.Iconize (False)
		self.removeTrayIcon()

	
	def onExit (self, event):
		self.mainWnd.Close()


	def CreatePopupMenu (self):
		trayMenu = wx.Menu()
		trayMenu.Append (self.ID_RESTORE, _(u"Restore"))
		trayMenu.Append (self.ID_EXIT, _(u"Exit"))

		return trayMenu


	def ShowIcon (self):
		self.SetIcon(self.icon)

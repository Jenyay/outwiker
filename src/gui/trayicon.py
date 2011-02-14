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

		self.__bind()

		self.initMainWnd()
		self.updateTrayIcon()
	

	def updateTrayIcon (self):
		"""
		Показать или скрыть иконку в трее в зависимости от настроек
		"""
		if Application.config.alwaysShowTrayIconOption.value:
			# Если установлена эта опция, то иконку показываем всегда
			self.ShowTrayIcon()
			return

		if Application.config.minimizeOption.value and self.mainWnd.IsIconized():
			self.ShowTrayIcon()
		else:
			self.removeTrayIcon()
	

	def __bind (self):
		self.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.OnTrayLeftClick)
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onRestore, id=self.ID_RESTORE)
		self.mainWnd.Bind (wx.EVT_ICONIZE, self.onIconize)
	

	def __unbind (self):
		self.Unbind (wx.EVT_TASKBAR_LEFT_DOWN, handler = self.OnTrayLeftClick)
		self.Unbind(wx.EVT_MENU, handler = self.onExit, id=self.ID_EXIT)
		self.Unbind(wx.EVT_MENU, handler = self.onRestore, id=self.ID_RESTORE)
		self.mainWnd.Unbind (wx.EVT_ICONIZE, handler = self.onIconize)


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
			self.ShowTrayIcon()
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
		if not Application.config.alwaysShowTrayIconOption.value:
			self.removeTrayIcon()

	
	def onExit (self, event):
		self.mainWnd.Close()


	def CreatePopupMenu (self):
		trayMenu = wx.Menu()
		trayMenu.Append (self.ID_RESTORE, _(u"Restore"))
		trayMenu.Append (self.ID_EXIT, _(u"Exit"))

		return trayMenu


	def Destroy (self):
		self.removeTrayIcon()
		self.__unbind()


	def ShowTrayIcon (self):
		if not self.IsIconInstalled():
			self.SetIcon(self.icon)

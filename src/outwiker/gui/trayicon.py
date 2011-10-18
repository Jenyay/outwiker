#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import wx

import outwiker.core.system
from outwiker.core.application import Application
from .guiconfig import TrayConfig


class OutwikerTrayIcon (wx.TaskBarIcon):
	"""
	Класс для работы с иконкой в трее
	"""
	def __init__ (self, mainWnd):
		wx.TaskBarIcon.__init__ (self)
		self.mainWnd = mainWnd
		self.config = TrayConfig (Application.config)

		self.ID_RESTORE = wx.NewId()
		self.ID_EXIT = wx.NewId()

		self.icon = wx.Icon(os.path.join (outwiker.core.system.getImagesDir(), "outwiker_16x16.png"), wx.BITMAP_TYPE_ANY)

		self.__bind()

		self.__initMainWnd()
		self.updateTrayIcon()
	

	def updateTrayIcon (self):
		"""
		Показать или скрыть иконку в трее в зависимости от настроек
		"""
		if self.config.alwaysShowTrayIconOption.value:
			# Если установлена эта опция, то иконку показываем всегда
			self.ShowTrayIcon()
			return

		if self.config.minimizeOption.value and self.mainWnd.IsIconized():
			self.ShowTrayIcon()
		else:
			self.removeTrayIcon()
	

	def __bind (self):
		self.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.__OnTrayLeftClick)
		self.Bind(wx.EVT_MENU, self.__onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.__onRestore, id=self.ID_RESTORE)
		self.mainWnd.Bind (wx.EVT_ICONIZE, self.__onIconize)
		Application.onPreferencesDialogClose += self.__onPreferencesDialogClose
	

	def __unbind (self):
		self.Unbind (wx.EVT_TASKBAR_LEFT_DOWN, handler = self.__OnTrayLeftClick)
		self.Unbind(wx.EVT_MENU, handler = self.__onExit, id=self.ID_EXIT)
		self.Unbind(wx.EVT_MENU, handler = self.__onRestore, id=self.ID_RESTORE)
		self.mainWnd.Unbind (wx.EVT_ICONIZE, handler = self.__onIconize)
		Application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
	

	def __onPreferencesDialogClose (self, prefDialog):
		self.updateTrayIcon()


	def __initMainWnd (self):
		if self.config.startIconizedOption.value:
			self.__iconizeWindow()
		else:
			self.mainWnd.Show()
	

	def __onIconize (self, event):
		if event.Iconized():
			# Окно свернули
			self.__iconizeWindow ()
		else:
			self.restoreWindow()

		self.updateTrayIcon()
	

	def __iconizeWindow (self):
		"""
		Свернуть окно
		"""
		if self.config.minimizeOption.value:
			# В трей добавим иконку, а окно спрячем
			self.ShowTrayIcon()
			self.mainWnd.Hide()


	def removeTrayIcon (self):
		"""
		Удалить иконку из трея
		"""
		if self.IsIconInstalled():
			self.RemoveIcon()


	def __onRestore (self, event):
		self.restoreWindow()


	def __OnTrayLeftClick (self, event):
		if self.mainWnd.IsIconized():
			self.restoreWindow()
		else:
			self.mainWnd.Iconize()
	

	def restoreWindow (self):
		self.mainWnd.Show ()
		self.mainWnd.Iconize (False)
		if not self.config.alwaysShowTrayIconOption.value:
			self.removeTrayIcon()

	
	def __onExit (self, event):
		self.mainWnd.Close()


	def CreatePopupMenu (self):
		trayMenu = wx.Menu()
		trayMenu.Append (self.ID_RESTORE, _(u"Restore"))
		trayMenu.Append (self.ID_EXIT, _(u"Exit"))

		return trayMenu


	def Destroy (self):
		self.removeTrayIcon()
		self.__unbind()
		wx.TaskBarIcon.Destroy (self)


	def ShowTrayIcon (self):
		if not self.IsIconInstalled():
			self.SetIcon(self.icon)

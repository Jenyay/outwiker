#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.commands import MessageBox
from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.core.pluginbase import Plugin


class PluginDebug (Plugin):
	def __init__ (self, application):
		Plugin.__init__ (self, application)


	def __createMenu (self):
		self.menu = wx.Menu (u"")
		self.menu.Append (self.ID_PLUGINSLIST, _(u"Plugins List"))
		self.menu.Append (self.ID_BUTTONSDIALOG, _(u"ButtonsDialog"))

		self._application.mainWindow.mainMenu.Append (self.menu, self.__menuName)

		self._application.mainWindow.Bind(wx.EVT_MENU, self.__onPluginsList, id=self.ID_PLUGINSLIST)
		self._application.mainWindow.Bind(wx.EVT_MENU, self.__onButtonsDialog, id=self.ID_BUTTONSDIALOG)


	def __onButtonsDialog (self, event):
		buttons = [_(u"Button 1"), _(u"Button 2"), _(u"Button 3"), _(u"Cancel")]
		with ButtonsDialog (self._application.mainWindow, _(u"Message"), _(u"Caption"), buttons, default=0, cancel=3) as dlg:
			result = dlg.ShowModal()

			if result == wx.ID_CANCEL:
				print u"Cancel"
			else:
				print result


	def __onPluginsList (self, event):
		pluginslist = [plugin.name + "\n" for plugin in self._application.plugins]
		MessageBox (u"".join (pluginslist), _(u"Plugins List"))


	###################################################
	# Свойства и методы, которые необходимо определить
	###################################################


	@property
	def name (self):
		return u"Debug Plugin"

	
	@property
	def description (self):
		return _(u"Debug Plugin")


	@property
	def version (self):
		return u"0.1"


	def initialize(self):
		domain = u"testdebug"

		langdir = os.path.join (os.path.dirname (__file__), "locale")
		global _

		try:
			_ = self._init_i18n (domain, langdir)
		except BaseException as e:
			print e
			raise

		self.ID_PLUGINSLIST = wx.NewId()
		self.ID_BUTTONSDIALOG = wx.NewId()

		self.__menuName = _(u"Debug")
		self.__createMenu()


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		self._application.mainWindow.Unbind(wx.EVT_MENU, handler=self.__onPluginsList, id=self.ID_PLUGINSLIST)
		self._application.mainWindow.Unbind(wx.EVT_MENU, handler=self.__onButtonsDialog, id=self.ID_BUTTONSDIALOG)

		index = self._application.mainWindow.mainMenu.FindMenu (self.__menuName)
		assert index != wx.NOT_FOUND

		index = self._application.mainWindow.mainMenu.Remove (index)

	#############################################

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import gettext

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.i18n import getLanguageFromConfig
from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.core.pluginbase import Plugin


class PluginDebug (Plugin):
	def __init__ (self, application):
		Plugin.__init__ (self, application)

		#self._application = application

		try:
			self.__init_i18n ()
		except BaseException as e:
			print e
			raise

		self.ID_PLUGINSLIST = wx.NewId()
		self.ID_BUTTONSDIALOG = wx.NewId()

		self.__createMenu()


	def __init_i18n (self):
		langdir = os.path.join (os.path.dirname (__file__), u'locale')
		language =  getLanguageFromConfig (self._application.config)

		global _

		try:
			lang = gettext.translation(u'testdebug', langdir, languages=[language])
		except IOError:
			lang = gettext.translation(u'testdebug', langdir, languages=["en"])

		_ = lang.ugettext


	def __createMenu (self):
		self.menu = wx.Menu (u"")
		self.menu.Append (self.ID_PLUGINSLIST, _(u"Plugins List"))
		self.menu.Append (self.ID_BUTTONSDIALOG, _(u"ButtonsDialog"))

		self._application.mainWindow.mainMenu.Append (self.menu, _(u"Debug"))

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


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"Debug Plugin"

	
	@property
	def description (self):
		return _(u"Debug Plugin")


	@property
	def version (self):
		return u"0.1"


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		pass

	#############################################

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import gettext

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.i18n import getLanguageFromConfig


class PluginDebug (object):
	def __init__ (self, application):
		self.__application = application

		try:
			self.__init_i18n ()
		except BaseException as e:
			print e
			raise

		self.ID_PLUGINSLIST = wx.NewId()

		self.__createMenu()


	def __init_i18n (self):
		langdir = os.path.join (os.path.dirname (__file__), u'locale')
		language =  getLanguageFromConfig (self.__application.config)

		global _

		try:
			lang = gettext.translation(u'testdebug', langdir, languages=[language])
		except IOError:
			lang = gettext.translation(u'testdebug', langdir, languages=["en"])

		_ = lang.ugettext


	def __createMenu (self):
		self.menu = wx.Menu (u"")
		self.menu.Append (self.ID_PLUGINSLIST, _(u"Plugins List"))

		self.__application.mainWindow.mainMenu.Append (self.menu, _(u"Debug"))

		self.__application.mainWindow.Bind(wx.EVT_MENU, self.__onPluginsList, id=self.ID_PLUGINSLIST)


	def __onPluginsList (self, event):
		pluginslist = [plugin.name + "\n" for plugin in self.__application.plugins]
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

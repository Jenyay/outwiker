#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import wx.html

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig
#from outwiker.core.pluginbase import Plugin


class PluginsPanel (wx.Panel):
	"""
	Панель со списком установленных плагинов
	"""
	def __init__ (self, parent):
		wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)
		self.__createGui ()

		self.__controller = PluginsController (self)


	def __createGui (self):
		self.pluginsList = wx.CheckListBox (self, -1, style=wx.LB_SORT)
		self.pluginsList.SetMinSize ((50, -1))

		self.pluginsInfo = wx.html.HtmlWindow (self, style=wx.html.HW_SCROLLBAR_AUTO)
		self.pluginsInfo.SetMinSize ((50, -1))

		self.__layout()

	
	def __layout (self):
		mainSizer = wx.FlexGridSizer (1, 2)
		mainSizer.AddGrowableRow (0)
		mainSizer.AddGrowableCol (0)
		mainSizer.AddGrowableCol (1)
		mainSizer.Add (self.pluginsList, flag=wx.EXPAND)
		mainSizer.Add (self.pluginsInfo, flag=wx.EXPAND)

		self.SetSizer (mainSizer)


	def LoadState(self):
		self.__controller.loadState ()


	def Save (self):
		self.__controller.save()



class PluginsController (object):
	"""
	Контроллер, отвечающий за работу панели со списком плагинов
	"""
	def __init__ (self, pluginspanel):
		self.__owner = pluginspanel

		self.__owner.Bind (wx.EVT_LISTBOX, self.__onSelectItem, self.__owner.pluginsList)


	def __onSelectItem (self, event):
		htmlContent = u""
		if event.IsSelection():
			plugin = event.GetClientData()
			assert plugin != None

			htmlContent = self.__createPluginInfo (plugin)

		self.__owner.pluginsInfo.SetPage (htmlContent)


	def __createPluginInfo (self, plugin):
		assert plugin != None
		#assert issubclass (plugin, Plugin)

		infoTemplate = _(u"""<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>

<BODY>
<H3>{name}</H3>
<B>Version:</B> {version}<BR>
<B>Description:</B> {description}
</BODY>
</HTML>""")

		description = plugin.description.replace ("\n", "<BR>")

		result = infoTemplate.format (name=plugin.name, version=plugin.version, description=description)
		return result


	def loadState (self):
		self.__owner.pluginsList.Clear()
		self.__appendEnabledPlugins()
		self.__appendDisabledPlugins()


	def __appendEnabledPlugins (self):
		"""
		Добавить загруженные плагины в список
		"""
		for plugin in Application.plugins:
			index = self.__owner.pluginsList.Append (plugin.name, plugin)
			assert self.__owner.pluginsList.GetClientData (index) == plugin

			self.__owner.pluginsList.Check (index)


	def __appendDisabledPlugins (self):
		"""
		Добавить отключенные плагины в список
		"""
		for plugin in Application.plugins.disabledPlugins.values():
			index = self.__owner.pluginsList.Append (plugin.name, plugin)
			assert self.__owner.pluginsList.GetClientData (index) == plugin

			self.__owner.pluginsList.Check (index, False)


	def save (self):
		config = PluginsConfig (Application.config)
		config.disabledPlugins.value = self.__getDisabledPlugins()
		Application.plugins.updateDisableList()


	def __getDisabledPlugins (self):
		disabledList = []

		for itemindex in range (self.__owner.pluginsList.GetCount()):
			if not self.__owner.pluginsList.IsChecked (itemindex):
				disabledList.append (self.__owner.pluginsList.GetClientData (itemindex).name)

		return disabledList


# -*- coding: UTF-8 -*-

import wx

from .i18n import get_
from .preferencesController import PreferencesController

class PreferencesPanel (wx.Panel):
	def __init__ (self, parent, config):
		wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)

		global _
		_ = get_()

		self.__createGui()
		self.__controller = PreferencesController (self, config)

	def __createGui(self):
		mainSizer = wx.FlexGridSizer (cols=1)
		mainSizer.AddGrowableCol (0)

		self.autoRenameAllPagesCheckBox = wx.CheckBox (self, label=_(u"Automatically rename all pages according to their first line"))
		mainSizer.Add(self.autoRenameAllPagesCheckBox, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)

		self.autoAddFirstLineCheckBox = wx.CheckBox (self, label=_(u"Automatically set first line of the page be the name of this page on page create"))
		mainSizer.Add(self.autoAddFirstLineCheckBox, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)

		self.SetSizer(mainSizer)
		self.Layout()

	def LoadState(self):
		self.__controller.loadState()

	def Save (self):
		self.__controller.save()

# -*- coding: UTF-8 -*-

from .i18n import get_
from .config import PluginConfig

class PreferencesController (object):
	def __init__ (self, owner, config):
		self.__owner = owner
		self.__config = PluginConfig (config)

		global _
		_ = get_()

	def loadState (self):
		self.__owner.autoRenameAllPagesCheckBox.SetValue (self.__config.autoRenameAllPages)
		self.__owner.autoAddFirstLineCheckBox.SetValue (self.__config.autoSetFirstLine)

	def save (self):
		self.__config.autoRenameAllPages = self.__owner.autoRenameAllPagesCheckBox.IsChecked()
		self.__config.autoSetFirstLine = self.__owner.autoAddFirstLineCheckBox.IsChecked()

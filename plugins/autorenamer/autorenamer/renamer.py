# -*- coding: UTF-8 -*-
from outwiker.core.commands import testPageTitle, renamePage
from .config import PluginConfig

class Renamer (object):
	def __init__ (self, application):
		self._application = application

	def RenamePage (self, manual=False):
		config = PluginConfig (self._application.config)
		if config.autoRenameAllPages or manual:
			currentPage = self._application.selectedPage
			if currentPage is not None and not currentPage.content == "":
				text = currentPage.content.splitlines()[0]
				text = self.getValidName(text)
				if not text == "" and text != currentPage.title:
					if testPageTitle (text) == True:
						renamePage(currentPage, text)
		if config.autoSetFirstLine:
			currentPage = self._application.selectedPage
			if currentPage is not None and currentPage.content == "":
				currentPage.content = currentPage.title

	def getValidName (self, name):
		name = "".join(char for char in name if char not in "\/:*?<>|!")
		while name[-1] in " .":
			name = name[0:len(name)-1]
		return name

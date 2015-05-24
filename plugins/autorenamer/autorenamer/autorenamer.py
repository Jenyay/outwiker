# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from .actions import AddAutoRenameTagAction 
from .preferencesPanel import PreferencesPanel
from .commands import AutoRenameTagCommand
from .renamer import Renamer

from i18n import get_

class AutoRenamer (object):
	def __init__ (self, plugin, application):
		self._application = application
		self._plugin = plugin
		self.ID_ADDAUTORENAMETAG = wx.NewId()
		self._menu = None

	def initialize (self):
		global _
		_ = get_()

		self._renamer = Renamer(self._application)

		self._application.onForceSave += self._renamer.RenamePage
		self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
		self._application.onPageViewCreate += self.__onPageViewCreate
		self._application.onPageViewDestroy += self.__onPageViewDestroy
		self._application.onWikiParserPrepare += self.__onWikiParserPrepare

	def destroy (self):
		self._application.onForceSave -= self._renamer.RenamePage
		self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
		self._application.onPageViewCreate -= self.__onPageViewCreate
		self._application.onPageViewDestroy -= self.__onPageViewDestroy
		self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

	def __onPreferencesDialogCreate (self, dialog):
		prefPanel = PreferencesPanel (dialog.treeBook, self._application.config)
		panelName = _(u"AutoRenamer [Plugin]")
		panelList = [PreferencePanelInfo (prefPanel, panelName)]
		dialog.appendPreferenceGroup (panelName, panelList)

	def __onPageViewCreate (self, page):
		assert self._application.mainWindow is not None

		if page.getTypeString() == u"wiki":
			self.addMenuItem()
			self._application.mainWindow.pagePanel.pageView.Bind (EVT_PAGE_TAB_CHANGED, self._onTabChanged)
			self.enableMenu()

	def __onPageViewDestroy (self, page):
		assert self._application.mainWindow is not None

		if page.getTypeString() == u"wiki":
			self.removeMenuItem()
			self._application.mainWindow.pagePanel.pageView.Unbind (EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)

	def _onTabChanged(self, event):
		self.enableMenu()
		event.Skip()

	def __onWikiParserPrepare (self, parser):
		parser.addCommand (AutoRenameTagCommand(self._application, parser))

	def enableMenu(self):
		pageView = self._application.mainWindow.pagePanel.pageView
		enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)
		self._application.actionController.enableTools (AddAutoRenameTagAction.stringId, enabled)
	

	def addMenuItem (self):
		self._application.actionController.register (AddAutoRenameTagAction (self._application), None)
		if self._application.mainWindow is not None:
			self._menu = wx.Menu()
			self._submenuItem = self._application.mainWindow.pagePanel.pageView.toolsMenu.AppendSubMenu (self._menu, _(u"AutoRenamer"))
			self._application.actionController.appendMenuItem (AddAutoRenameTagAction.stringId, self._menu)

	def removeMenuItem (self):
		if self._application.mainWindow is not None:
			self._application.actionController.removeMenuItem (AddAutoRenameTagAction.stringId)
			self._application.mainWindow.pagePanel.pageView.toolsMenu.DestroyItem (self._submenuItem)
			self._submenuItem = None
			self._application.actionController.removeAction (AddAutoRenameTagAction.stringId)

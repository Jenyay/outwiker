# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from .i18n import get_

class BaseHeadAction (BaseAction):
	def __init__ (self, application):
		self._application = application

		global _
		_ = get_()

class AddAutoRenameTagAction (BaseHeadAction):
	stringId = u"AutoRenamer_AddAutoRenameTag"

	@property
	def title (self):
		return _(u"AutoRename (:autorename:)")

	@property
	def description (self):
		return _(u"Insert AutoRename (:autorename:) command")

	def run (self, params):
		self._application.mainWindow.pagePanel.pageView.codeEditor.AddText (u"(:autorename:)")

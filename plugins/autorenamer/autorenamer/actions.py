# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class AddAutoRenameTagAction(BaseAction):
    stringId = u"AutoRenamer_AddAutoRenameTag"

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"AutoRename (:autorename:)")

    @property
    def description(self):
        return _(u"Insert AutoRename (:autorename:) command")

    def run(self, params):
        self._application.mainWindow.pagePanel.pageView.codeEditor.AddText(u"(:autorename:)")

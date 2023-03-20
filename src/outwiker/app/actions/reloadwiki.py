# -*- coding: utf-8 -*-

import wx

from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.gui.baseaction import BaseAction
from outwiker.app.services.tree import openWiki


class ReloadWikiAction(BaseAction):
    """
    Перезагрузка wiki
    """
    stringId = "ReloadWiki"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Reload Wiki…")

    @property
    def description(self):
        return _("Reload wiki")

    def run(self, params):
        if self._application.wikiroot is not None:
            result = (MessageBox(_("Save current page before reload?"),
                                 _("Save?"), wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION))

            if result == wx.CANCEL:
                return

            self._application.mainWindow.destroyPagePanel(result == wx.YES)
            openWiki(self._application.wikiroot.path)

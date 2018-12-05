# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import MessageBox, openWiki


class ReloadWikiAction (BaseAction):
    """
    Перезагрузка wiki
    """
    stringId = u"ReloadWiki"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Reload Wiki…")

    @property
    def description(self):
        return _(u"Reload wiki")

    def run(self, params):
        if self._application.wikiroot is not None:
            result = (MessageBox(_(u"Save current page before reload?"),
                                 _(u"Save?"), wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION))

            if result == wx.CANCEL:
                return

            self._application.mainWindow.destroyPagePanel(result == wx.YES)
            openWiki(self._application.wikiroot.path)

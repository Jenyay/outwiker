# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, MessageBox
from outwiker.pages.search.searchpage import GlobalSearch


class GlobalSearchAction (BaseAction):
    """
    Создать страницу с глобальным поиском
    """
    stringId = u"GlobalSearch"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Global Search…")


    @property
    def description (self):
        return _(u"Create or open page for global search")


    def run (self, params):
        self._openGlobalSearch ()


    @testreadonly
    def _openGlobalSearch (self):
        if self._application.wikiroot is not None:
            try:
                GlobalSearch.create (self._application.wikiroot)
            except IOError:
                MessageBox (_(u"Can't create page"),
                            _(u"Error"),
                            wx.ICON_ERROR | wx.OK)

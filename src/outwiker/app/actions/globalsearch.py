# -*- coding: utf-8 -*-

from outwiker.app.services.messages import showError
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction
from outwiker.pages.search.searchpage import GlobalSearch


class GlobalSearchAction (BaseAction):
    """
    Создать страницу с глобальным поиском
    """
    stringId = "GlobalSearch"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Global Search…")

    @property
    def description(self):
        return _("Create or open page for global search")

    def run(self, params):
        self._openGlobalSearch()

    @testreadonly
    def _openGlobalSearch(self):
        if self._application.wikiroot is not None:
            try:
                GlobalSearch.create(self._application.wikiroot)
            except IOError:
                showError(self._application.mainWindow,
                          _("Can't create page"))

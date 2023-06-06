# -*- coding: utf-8 -*-

from outwiker.app.services.bookmarks import toggleBookmarkForCurrentPage
from outwiker.gui.baseaction import BaseAction


class AddBookmarkAction (BaseAction):
    """Добавить (удалить) страницу в (из) закладки."""

    stringId = 'AddBookmark'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('Add/Remove Bookmark')

    @property
    def description(self):
        return _('Add/Remove Bookmark')

    def run(self, params):
        toggleBookmarkForCurrentPage(self._application)

# -*- coding: utf-8 -*-

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
        if self._application.selectedPage is not None:
            wikiroot = self._application.wikiroot
            selected_page = wikiroot.selectedPage

            if wikiroot.bookmarks.pageMarked(selected_page):
                wikiroot.bookmarks.remove(selected_page)
            else:
                wikiroot.bookmarks.add(selected_page)

# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class AddBookmarkAction (BaseAction):
    """
    Добавить (удалить) страницу в (из) закладки
    """
    stringId = u"AddBookmark"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Add/Remove Bookmark")


    @property
    def description (self):
        return _(u"Add/Remove Bookmark")


    def run (self, params):
        if self._application.selectedPage is not None:
            wikiroot = self._application.wikiroot
            selectedPage = wikiroot.selectedPage

            if not wikiroot.bookmarks.pageMarked (selectedPage):
                wikiroot.bookmarks.add (selectedPage)
            else:
                wikiroot.bookmarks.remove (selectedPage)

# -*- coding: utf-8 -*-

from typing import List, Optional

from outwiker.core.tree import BasePage, WikiDocument
from .event import Event
from .events import BookmarksChangedParams
from .config import StringListSection


class Bookmarks:
    """
    Класс, хранящий избранные страницы внутри вики
    """
    CONFIG_SECTION = "Bookmarks"
    CONFIG_OPTION = "bookmark_"

    def __init__(self):
        self._wikiroot: Optional[WikiDocument] = None
        self._pages: List[str] = []
        self._config = None

        # Изменение списка закладок
        # Параметр - экземпляр класса Bookmarks
        self.onBookmarksChanged = Event()

    def clear(self):
        self.setWikiRoot(None)

    def setWikiRoot(self, wikiroot: Optional[WikiDocument]):
        self._wikiroot = wikiroot
        self._pages.clear()
        self._config = None

        if self._wikiroot is not None:
            self._config = StringListSection(self._wikiroot.params, Bookmarks.CONFIG_SECTION, Bookmarks.CONFIG_OPTION)
            self._pages = self._config.value

    def pageRenamed(self, page, oldSubpath):
        for n in range(len(self._pages)):
            subpath = self._pages[n]
            if subpath.startswith(oldSubpath):
                self._pages[n] = subpath.replace(oldSubpath, page.subpath, 1)
                self._save()

    def __len__(self) -> int:
        return len(self._pages)

    def __getitem__(self, index) -> Optional[BasePage]:
        if self._wikiroot is None:
            raise IndexError()

        subpath = self._pages[index]
        return self._wikiroot[subpath]

    def add(self, page):
        if page.subpath in self._pages:
            return

        self._pages.append(page.subpath)
        self._save()
        event_params = BookmarksChangedParams(
            bookmarks=self,
            page=page,
            action=BookmarksChangedParams.ACTION_ADD_TO_BOOKMARKS,
        )
        self.onBookmarksChanged(event_params)

    def _save(self):
        assert self._config is not None
        self._config.value = self._pages

    def remove(self, page):
        self._pages.remove(page.subpath)
        event_params = BookmarksChangedParams(
            bookmarks=self,
            page=page,
            action=BookmarksChangedParams.ACTION_REMOVE_FROM_BOOKMARKS,
        )
        self.onBookmarksChanged(event_params)
        self._save()

    def pageMarked(self, page):
        """
        Узнать находится ли страница в избранном
        """
        return page.subpath in self._pages

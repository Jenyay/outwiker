# -*- coding: utf-8 -*-

from typing import List, Optional

from outwiker.core.exceptions import ReadonlyException
from outwiker.core.tree import BasePage, WikiDocument, WikiPage
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

        page_id = self._pages[index]
        return self._getPage(page_id)

    def _getPage(self, page_id: str) -> Optional[BasePage]:
        """Get page by subpath or page UID"""
        if self._wikiroot is None:
            return None

        return self._wikiroot.getPageByUid(page_id) or self._wikiroot[page_id]

    def _getPageId(self, page: BasePage) -> Optional[str]:
        # if page.parent is None or page.isRemoved:
        #     return None

        if page.subpath in self._pages:
            return page.subpath

        try:
            page_uid = page.getUid(generate=False)
            if page_uid in self._pages:
                return page_uid
        except ReadonlyException:
            return None

        return None

    def add(self, page: WikiPage, subpath: bool = False):
        """
        Add page to bookmarks.

        subpath is used for backward compatibility in tests
        """
        if self.pageMarked(page):
            return

        if subpath:
            self._pages.append(page.subpath)
        else:
            self._pages.append(page.getUid(generate=True))

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
        page_id = self._getPageId(page)
        if page_id is not None:
            self._pages.remove(page_id)
            event_params = BookmarksChangedParams(
                bookmarks=self,
                page=page,
                action=BookmarksChangedParams.ACTION_REMOVE_FROM_BOOKMARKS,
            )
            self.onBookmarksChanged(event_params)
            self._save()

    def pageMarked(self, page: WikiPage):
        """
        Узнать находится ли страница в избранном
        """
        return self._getPageId(page) is not None

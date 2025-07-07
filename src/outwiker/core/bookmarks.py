# -*- coding: utf-8 -*-

from .event import Event
from .events import BookmarksChangedParams
from .config import StringListSection


class Bookmarks:
    """
    Класс, хранящий избранные страницы внутри вики
    """

    def __init__(self, wikiroot, config):
        """
        wikiroot -- корень вики
        config -- экземпляр класса Config, который будет хранить настройки
        """
        self.root = wikiroot
        self.configSection = "Bookmarks"
        self.configOption = "bookmark_"

        self.__bookmarksConfig = StringListSection(
            config, self.configSection, self.configOption
        )

        # Страницы в закладках
        self.__pages = self.__bookmarksConfig.value

        # Изменение списка закладок
        # Параметр - экземпляр класса Bookmarks
        self.onBookmarksChanged = Event()

        wikiroot.onPageRemove += self._onPageRemove
        wikiroot.onPageRename += self._onPageRename

    def _onPageRemove(self, page):
        """
        Обработчик события при удалении страниц
        """
        # Если удаляемая страница в закладках, то уберем ее оттуда
        if self.pageMarked(page):
            self.remove(page)

    def _onPageRename(self, page, oldSubpath):
        for n in range(len(self.__pages)):
            subpath = self.__pages[n]
            if subpath.startswith(oldSubpath):
                self.__pages[n] = subpath.replace(oldSubpath, page.subpath, 1)
                self.save()

    def __len__(self):
        return len(self.__pages)

    def __getitem__(self, index):
        subpath = self.__pages[index]
        return self.root[subpath]

    def add(self, page):
        if page.subpath in self.__pages:
            return

        self.__pages.append(page.subpath)
        self.save()
        event_params = BookmarksChangedParams(
            bookmarks=self,
            page=page,
            action=BookmarksChangedParams.ACTION_ADD_TO_BOOKMARKS,
        )
        self.onBookmarksChanged(event_params)

    def save(self):
        self.__bookmarksConfig.value = self.__pages

    def remove(self, page):
        self.__pages.remove(page.subpath)
        event_params = BookmarksChangedParams(
            bookmarks=self,
            page=page,
            action=BookmarksChangedParams.ACTION_REMOVE_FROM_BOOKMARKS,
        )
        self.onBookmarksChanged(event_params)
        self.save()

    def pageMarked(self, page):
        """
        Узнать находится ли страница в избранном
        """
        return page.subpath in self.__pages

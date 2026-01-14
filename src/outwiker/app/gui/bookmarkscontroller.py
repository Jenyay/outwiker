# -*- coding: utf-8 -*-

from typing import Dict, Optional
import wx

from outwiker.core.application import Application
from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.core.tree import WikiDocument, WikiPage
from outwiker.gui.defines import MENU_BOOKMARKS


class BookmarksController:
    """
    Класс для организации работы GUI с закладками
    """
    def __init__(self, mainWndController, application: Application):
        """
        mainWndController - экземпляр класса MainWndController
        """
        self.mainWndController = mainWndController
        self._application = application

        # Идентификаторы для пунктов меню для открытия закладок
        # Ключ - id, значение - путь до страницы вики
        self._bookmarksId: Dict[str, str] = {}

        self._application.onBookmarksChanged += self._onBookmarksChanged
        self._application.onWikiOpen.bind(self._onWikiOpen, EVENT_PRIORITY_MAX_CORE)
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onPageRemove += self._onPageRemove
        self._application.onPageRename += self._onPageRename

        self._updateBookmarksMenu()

    def clear(self):
        self._application.onBookmarksChanged -= self._onBookmarksChanged
        self._application.onWikiOpen -= self._onWikiOpen
        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onPageRemove -= self._onPageRemove
        self._application.onPageRename -= self._onPageRename

    def _onPageRemove(self, page):
        """
        Обработчик события при удалении страниц
        """
        # Если удаляемая страница в закладках, то уберем ее оттуда
        bookmarks = self._application.bookmarks

        if bookmarks.pageMarked(page):
            bookmarks.remove(page)

    def _onPageRename(self, page: WikiPage, oldSubpath: str):
        self._application.bookmarks.pageRenamed(page, oldSubpath)

    def _onTreeUpdate(self, sender):
        self._updateBookmarksMenu()

    def _onPageUpdate(self, page, **kwargs):
        self._updateBookmarksMenu()

    def _onWikiOpen(self, wikiroot: Optional[WikiDocument]):
        self._application.bookmarks.setWikiRoot(wikiroot)
        self._updateBookmarksMenu()

    def _onBookmarksChanged(self, params):
        self._updateBookmarksMenu()

    def _updateBookmarksMenu(self):
        menu_bookmarks = self.mainWndController.mainWindow.menuController[MENU_BOOKMARKS]
        self.mainWndController.removeMenuItemsById(
            menu_bookmarks,
            list(self._bookmarksId.keys())
        )
        self._bookmarksId.clear()

        for n in range(len(self._application.bookmarks)):
            control_id = wx.Window.NewControlId()
            page = self._application.bookmarks[n]
            if page is None:
                continue

            subpath = page.subpath
            self._bookmarksId[control_id] = subpath

            # Найдем родителя
            parentPage = page.parent

            if parentPage.parent is not None:
                label = "%s [%s]" % (page.display_title, parentPage.subpath)
            else:
                label = page.display_title

            menu_bookmarks.Append(control_id, label, "", wx.ITEM_NORMAL)
            self.mainWndController.mainWindow.Bind(wx.EVT_MENU,
                                                   self._onSelectBookmark,
                                                   id=control_id)

    def _onSelectBookmark(self, event):
        subpath = self._bookmarksId[event.Id]
        page = self._application.wikiroot[subpath]

        if page is not None:
            self._application.selectedPage = page

# -*- coding: utf-8 -*-

import wx

from outwiker.gui.defines import MENU_BOOKMARKS


class BookmarksController:
    """
    Класс для организации работы GUI с закладками
    """
    def __init__(self, mainWndController, application):
        """
        mainWndController - экземпляр класса MainWndController
        """
        self.mainWndController = mainWndController
        self._application = application

        # Идентификаторы для пунктов меню для открытия закладок
        # Ключ - id, значение - путь до страницы вики
        self._bookmarksId = {}

    def updateBookmarks(self):
        menu_bookmarks = self.mainWndController.mainWindow.menuController[MENU_BOOKMARKS]
        self.mainWndController.removeMenuItemsById(
            menu_bookmarks,
            list(self._bookmarksId.keys())
        )
        self._bookmarksId = {}

        if self._application.wikiroot is not None:
            for n in range(len(self._application.wikiroot.bookmarks)):
                control_id = wx.Window.NewControlId()
                page = self._application.wikiroot.bookmarks[n]
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
            self._application.wikiroot.selectedPage = self._application.wikiroot[subpath]

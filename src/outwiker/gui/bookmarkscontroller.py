# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from .defines import MENU_BOOKMARKS


class BookmarksController (object):
    """
    Класс для организации работы GUI с закладками
    """
    def __init__ (self, controller):
        """
        controller - экземпляр класса MainWndController
        """
        self.controller = controller

        # Идентификаторы для пунктов меню для открытия закладок
        # Ключ - id, значение - путь до страницы вики
        self._bookmarksId = {}


    def updateBookmarks (self):
        menu_bookmarks = self.controller.mainWindow.menuController[MENU_BOOKMARKS]
        self.controller.removeMenuItemsById (menu_bookmarks,
                                             list(self._bookmarksId.keys()))
        self._bookmarksId = {}

        if Application.wikiroot is not None:
            for n in range (len (Application.wikiroot.bookmarks)):
                id = wx.Window.NewControlId()
                page = Application.wikiroot.bookmarks[n]
                if page is None:
                    continue

                subpath = page.subpath
                self._bookmarksId[id] = subpath

                # Найдем родителя
                parentPage = page.parent

                if parentPage.parent is not None:
                    label = "%s [%s]" % (page.display_title, parentPage.subpath)
                else:
                    label = page.display_title

                menu_bookmarks.Append (id, label, "", wx.ITEM_NORMAL)
                self.controller.mainWindow.Bind(wx.EVT_MENU, self.__onSelectBookmark, id=id)


    def __onSelectBookmark (self, event):
        subpath = self._bookmarksId[event.Id]
        page = Application.wikiroot[subpath]

        if page is not None:
            Application.wikiroot.selectedPage = Application.wikiroot[subpath]

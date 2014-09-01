# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application


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
        self.controller.removeMenuItemsById (self.controller.mainMenu.bookmarksMenu, self._bookmarksId.keys())
        self._bookmarksId = {}

        if Application.wikiroot is not None:
            for n in range (len (Application.wikiroot.bookmarks)):
                id = wx.NewId()
                page = Application.wikiroot.bookmarks[n]
                if page is None:
                    continue

                subpath = page.subpath
                self._bookmarksId[id] = subpath

                # Найдем родителя
                parentPage = page.parent

                if parentPage.parent is not None:
                    label = "%s [%s]" % (page.title, parentPage.subpath)
                else:
                    label = page.title

                self.controller.mainMenu.bookmarksMenu.Append (id, label, "", wx.ITEM_NORMAL)
                self.controller.mainWindow.Bind(wx.EVT_MENU, self.__onSelectBookmark, id=id)

            self.controller.mainWindow.updateShortcuts()


    def __onSelectBookmark (self, event):
        subpath = self._bookmarksId[event.Id]
        page = Application.wikiroot[subpath]

        if page is not None:
            Application.wikiroot.selectedPage = Application.wikiroot[subpath]

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from .mainid import MainId


class BookmarksController (object):
    """
    Класс для организации работы GUI с закладками
    """
    def __init__ (self, controller):
        """
        parentWnd - указатель на главное окно
        """
        self.controller = controller

        # Идентификаторы для пунктов меню для открытия закладок
        # Ключ - id, значение - путь до страницы вики
        self._bookmarksId = {}

        self.controller.mainWindow.Bind(wx.EVT_MENU, self.__onBookmark, id=MainId.ID_ADDBOOKMARK)


    def updateBookmarks (self):
        self.controller.removeMenuItemsById (self.controller.mainMenu.bookmarksMenu, self._bookmarksId.keys())
        self._bookmarksId = {}

        if Application.wikiroot != None:
            for n in range (len (Application.wikiroot.bookmarks)):
                id = wx.NewId()
                page = Application.wikiroot.bookmarks[n]
                if page == None:
                    continue

                subpath = page.subpath
                self._bookmarksId[id] = subpath

                # Найдем родителя
                parentPage = page.parent

                if parentPage.parent != None:
                    label = "%s [%s]" % (page.title, parentPage.subpath)
                else:
                    label = page.title

                self.controller.mainMenu.bookmarksMenu.Append (id, label, "", wx.ITEM_NORMAL)
                self.controller.mainWindow.Bind(wx.EVT_MENU, self.__onSelectBookmark, id=id)


    def __onSelectBookmark (self, event):
        subpath = self._bookmarksId[event.Id]
        page = Application.wikiroot[subpath]

        if page != None:
            Application.wikiroot.selectedPage = Application.wikiroot[subpath]


    def __onBookmark(self, event):
        """
        Обработчик события при добавлении/удалении текущей страницы
        """
        if Application.selectedPage != None:
            selectedPage = Application.wikiroot.selectedPage

            if not Application.wikiroot.bookmarks.pageMarked (selectedPage):
                Application.wikiroot.bookmarks.add (Application.wikiroot.selectedPage)
            else:
                Application.wikiroot.bookmarks.remove (Application.wikiroot.selectedPage)

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx


class MenuMaker (object):
    """
    Класс добавляет пункты в контекстное меню
    """
    def __init__ (self, controller, menu, parent):
        """
        menu - контекстное меню
        parent - родительское окно, которое будет получать сообщение от меню
        """
        self._menu = menu
        self._parent = parent
        self._controller = controller

        # Словарь для нахождения инструмента по идентификатору меню
        # Ключ - id, значение - экземпляр ToolsInfo
        self._menuId = {}


    def insertContentMenuItem (self):
        """
        Добавить пункт меню для открытия файла контента во внешнем редакторе
        """
        # Меню для открытия файла с текстом
        contentMenu = wx.Menu()
        self.__appendToolsMenu (contentMenu, self.__onOpenContentFile, self._controller.tools)

        itemsCount = len (self._menu.GetMenuItems())
        self._menu.InsertMenu (itemsCount - 2, -1, _(u"Open Content File with..."), contentMenu, u"")


    def insertResultMenuItem (self):
        # Меню для открытия файла с результатом (HTML)
        resultMenu = wx.Menu()
        self.__appendToolsMenu (resultMenu, self.__onOpenResultFile, self._controller.tools)

        itemsCount = len (self._menu.GetMenuItems())
        self._menu.InsertMenu (itemsCount - 2, -1, _(u"Open Result HTML File with..."), resultMenu, u"")


    def __appendToolsMenu (self, menu, function, tools):
        """
        Добавить пункты для внешних редакторов
        menu - добавляемое контекстное меню
        function - обработчик события выбора пункта меню
        """
        for toolItem in tools:
            menuId = wx.NewId()

            menuItem = menu.Append (menuId, toolItem.title)
            self._parent.Bind (wx.EVT_MENU, id=menuId, handler=function)
            self._menuId[menuId] = toolItem


    def __unbindAll (self):
        """
        Отписать родительское окно от всех событий, связанных с инструментами
        """
        for menuId in self._menuId:
            self._parent.Unbind (wx.EVT_MENU, id=menuId)

        self._menuId = {}


    def __onOpenContentFile (self, event):
        self._controller.openContentFile (self._menuId[event.GetId()])
        self.__unbindAll()
    

    def __onOpenResultFile (self, event):
        self._controller.openResultFile (self._menuId[event.GetId()])
        self.__unbindAll()



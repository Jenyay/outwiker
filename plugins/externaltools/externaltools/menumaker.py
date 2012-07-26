#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx


class MenuMaker (object):
    """
    Класс добавляет пункты в контекстное меню
    """
    def __init__ (self, menu, tools):
        """
        menu - контекстное меню
        tools - список ToolsInfo для внешних редакторов
        """
        self._menu = menu
        self._tools = tools


    def insertContentMenuItem (self, openContentFileFunction):
        """
        Добавить пункт меню для открытия файла контента во внешнем редакторе
        """
        # Меню для открытия файла с текстом
        contentMenu = wx.Menu()
        self.__appendToolsMenu (contentMenu, openContentFileFunction, self._tools)

        itemsCount = len (self._menu.GetMenuItems())
        self._menu.InsertMenu (itemsCount - 2, -1, _(u"Open Content File with..."), contentMenu, u"")


    def insertResultMenuItem (self, openResultFileFunction):
        # Меню для открытия файла с результатом (HTML)
        resultMenu = wx.Menu()
        self.__appendToolsMenu (resultMenu, openResultFileFunction, self._tools)

        itemsCount = len (self._menu.GetMenuItems())
        self._menu.InsertMenu (itemsCount - 2, -1, _(u"Open Result HTML File with..."), resultMenu, u"")


    def __appendToolsMenu (self, menu, function, tools):
        """
        Добавить пункты для внешних редакторов
        menu - добавляемое контекстное меню
        function - обработчик события выбора пункта меню
        """
        for toolItem in tools:
            menuItem = menu.Append (toolItem.toolsid, toolItem.title)
            menu.Bind (wx.EVT_MENU, id=toolItem.toolsid, handler=function)

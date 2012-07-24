#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from toolsinfo import ToolsInfo


class Controller (object):
    """
    Этот класс отвечает за основную работу плагина
    """
    def __init__ (self, ownerPlugin):
        self._owner = ownerPlugin

        self._tools = [ToolsInfo (u"gvim", u"gvim", wx.NewId()), 
                ToolsInfo (u"scite", u"scite", wx.NewId())]

        self._page = None


    def initialize (self):
        self._owner.application.onTreePopupMenu += self.__onTreePopupMenu


    def destroy (self):
        self._owner.application.onTreePopupMenu -= self.__onTreePopupMenu


    def __onTreePopupMenu (self, menu, page):
        self._page = page

        if page.getTypeString() == "wiki":
            self.__insertWikiItems (menu)


    def __insertWikiItems (self, menu):
        contentMenu = wx.Menu()
        self.__appendToolsMenu (contentMenu, self.__onOpenContentFile)

        itemsCount = len (menu.GetMenuItems())
        menu.InsertMenu (itemsCount - 3, -1, _(u"Open Content File with..."), contentMenu, u"")


    def __onOpenContentFile (self, event):
        tools = None
        for toolItem in self._tools:
            if toolItem.toolsid == event.GetId():
                tools = toolItem
                break

        assert tools != None
        print tools.title


    def __appendToolsMenu (self, menu, function):
        """
        Добавить пункты для внешних редакторов
        menu - добавляемое контекстное меню
        function - обработчик события выбора пункта меню
        """
        for toolItem in self._tools:
            menuItem = menu.Append (toolItem.toolsid, toolItem.title)
            menu.Bind (wx.EVT_MENU, id=toolItem.toolsid, handler=function)


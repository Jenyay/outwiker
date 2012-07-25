#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import subprocess

import wx

from outwiker.core.tree import RootWikiPage

from .toolsinfo import ToolsInfo
from .menumaker import MenuMaker


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
        menuMaker = MenuMaker (menu, self._tools)

        if page.getTypeString() == "wiki":
            menuMaker.insertWikiItems (self.__onOpenContentFile, self.__onOpenResultFile)


    def __onOpenContentFile (self, event):
        assert self._page != None

        tools = self.__getToolsById (event.GetId())
        contentFname = os.path.join (self._page.path, RootWikiPage.contentFile)

        self.__executeTools (tools.command, contentFname)


    def __onOpenResultFile (self, event):
        assert self._page != None

        tools = self.__getToolsById (event.GetId())
        contentFname = os.path.join (self._page.path, "__content.html")

        self.__executeTools (tools.command, contentFname)


    def __executeTools (self, command, fname):
        subprocess.call ([command, fname])


    def __getToolsById (self, toolsid):
        tools = None

        for toolItem in self._tools:
            if toolItem.toolsid == toolsid:
                tools = toolItem
                break

        assert tools != None
        return tools

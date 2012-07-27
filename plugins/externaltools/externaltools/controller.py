#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import subprocess

import wx

from outwiker.core.tree import RootWikiPage
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.core.commands import MessageBox

from .toolsinfo import ToolsInfo
from .menumaker import MenuMaker
from .toolsconfig import ToolsConfig


class Controller (object):
    """
    Этот класс отвечает за основную работу плагина
    """
    def __init__ (self, ownerPlugin):
        self._owner = ownerPlugin

        self._page = None
        self._toolsConfig = ToolsConfig (self._owner.application.config)
        self._tools = None


    def initialize (self):
        self._owner.application.onTreePopupMenu += self.__onTreePopupMenu
        self._owner.application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate


    def destroy (self):
        self._owner.application.onTreePopupMenu -= self.__onTreePopupMenu
        self._owner.application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate


    def __onTreePopupMenu (self, menu, page):
        self._page = page
        self._tools = self._toolsConfig.tools

        menuMaker = MenuMaker (menu, self._tools)
        pagetype = page.getTypeString()

        if pagetype == "wiki" or pagetype == "html":
            menuMaker.insertContentMenuItem (self.__onOpenContentFile)
            menuMaker.insertResultMenuItem (self.__onOpenResultFile)        
        elif pagetype == "text":
            menuMaker.insertContentMenuItem (self.__onOpenContentFile)


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
        try:
            subprocess.call ([command, fname])
        except OSError:
            MessageBox (_(u"Can't execute tools"), 
                    _(u"Error"),
                    wx.OK | wx.ICON_ERROR )


    def __getToolsById (self, toolsid):
        tools = None

        for toolItem in self._tools:
            if toolItem.toolsid == toolsid:
                tools = toolItem
                break

        assert tools != None
        return tools


    def __onPreferencesDialogCreate (self, dialog):
        from .preferencespanel import PreferencesPanel
        prefPanel = PreferencesPanel (dialog.treeBook, self._owner.application.config)

        panelName = _(u"External Tools [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)

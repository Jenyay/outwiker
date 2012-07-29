#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import subprocess

import wx

from outwiker.core.tree import RootWikiPage
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.core.commands import MessageBox
from outwiker.core.system import getOS

from .toolsinfo import ToolsInfo
from .menumaker import MenuMaker
from .toolsconfig import ToolsConfig
from .i18n import get_


class Controller (object):
    """
    Этот класс отвечает за основную работу плагина
    """
    def __init__ (self, ownerPlugin):
        self._owner = ownerPlugin

        self._page = None
        self._toolsConfig = ToolsConfig (self._owner.application.config)


    @property
    def tools (self):
        return self._toolsConfig.tools


    def initialize (self):
        global _
        _ = get_()

        self._owner.application.onTreePopupMenu += self.__onTreePopupMenu
        self._owner.application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate


    def destroy (self):
        self._owner.application.onTreePopupMenu -= self.__onTreePopupMenu
        self._owner.application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate


    def __onTreePopupMenu (self, menu, page):
        self._page = page

        menuMaker = MenuMaker (self, menu, self._owner.application.mainWindow)
        pagetype = page.getTypeString()

        if pagetype == "wiki" or pagetype == "html":
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem ()
            menuMaker.insertResultMenuItem ()
        elif pagetype == "text":
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem ()


    def openContentFile (self, tools):
        """
        Открыть файл контента текущей страницы с помощью tools
        """
        assert self._page != None
        contentFname = os.path.join (self._page.path, RootWikiPage.contentFile)
        self.__executeTools (tools.command, contentFname)


    def openResultFile (self, tools):
        """
        Открыть файл результата текущей страницы с помощью tools
        """
        assert self._page != None
        contentFname = os.path.join (self._page.path, "__content.html")
        self.__executeTools (tools.command, contentFname)


    def __executeTools (self, command, fname):
        encoding = getOS().filesEncoding

        try:
            subprocess.call ([command.encode (encoding), 
                fname.encode (encoding)])
        except OSError:
            MessageBox (_(u"Can't execute tools"), 
                    _(u"Error"),
                    wx.OK | wx.ICON_ERROR )


    def __onPreferencesDialogCreate (self, dialog):
        from .preferencespanel import PreferencesPanel
        prefPanel = PreferencesPanel (dialog.treeBook, self._owner.application.config)

        panelName = _(u"External Tools [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)

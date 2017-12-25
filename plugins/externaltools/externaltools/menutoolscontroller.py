# -*- coding: utf-8 -*-

import os.path
import subprocess

import wx

from outwiker.core.tree import RootWikiPage
from outwiker.core.commands import MessageBox

from .i18n import get_
from .menumaker import MenuMaker
from .config import ExternalToolsConfig


class MenuToolsController(object):
    def __init__(self, application):
        self._application = application
        self._toolsConfig = ExternalToolsConfig(self._application.config)

        self._page = None

    @property
    def tools(self):
        return self._toolsConfig.tools

    def initialize(self):
        global _
        _ = get_()

        self._application.onTreePopupMenu += self.__onTreePopupMenu

    def destroy(self):
        self._application.onTreePopupMenu -= self.__onTreePopupMenu

    def __onTreePopupMenu(self, menu, page):
        self._page = page

        menuMaker = MenuMaker(self, menu, self._application.mainWindow)
        pagetype = page.getTypeString()

        if(pagetype == u"wiki" or
                pagetype == u"html" or
                pagetype == u"markdown"):
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem()
            menuMaker.insertResultMenuItem()
        elif pagetype == u"text":
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem()

    def openContentFile(self, tools):
        """
        Открыть файл контента текущей страницы с помощью tools
        """
        assert self._page is not None
        contentFname = os.path.join(self._page.path, RootWikiPage.contentFile)
        self.__executeTools(tools.command, contentFname)

    def openResultFile(self, tools):
        """
        Открыть файл результата текущей страницы с помощью tools
        """
        assert self._page is not None
        contentFname = os.path.join(self._page.path, "__content.html")
        self.__executeTools(tools.command, contentFname)

    def __executeTools(self, command, fname):
        try:
            subprocess.call([command, fname])
        except OSError:
            MessageBox(_(u"Can't execute tools"),
                       _(u"Error"),
                       wx.OK | wx.ICON_ERROR)

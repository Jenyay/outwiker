# -*- coding: utf-8 -*-

import os.path
import subprocess

import wx

from outwiker.api.core.defines import PAGE_CONTENT_FILE
from outwiker.api.gui.dialogs.messagebox import MessageBox

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

        if pagetype == "wiki" or pagetype == "html" or pagetype == "markdown":
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem()
            menuMaker.insertResultMenuItem()
        elif pagetype == "text":
            menuMaker.insertSeparator()
            menuMaker.insertContentMenuItem()

    def openContentFile(self, tools):
        """
        Открыть файл контента текущей страницы с помощью tools
        """
        assert self._page is not None
        contentFname = os.path.join(self._page.path, PAGE_CONTENT_FILE)
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
            MessageBox(_("Can't execute tools"), _("Error"), wx.OK | wx.ICON_ERROR)

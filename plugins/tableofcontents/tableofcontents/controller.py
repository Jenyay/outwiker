# -*- coding: utf-8 -*-

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo)

from .i18n import get_
from .commands import TOCCommand
from .actions import GenerateTOC, InsertTOCCommand
from . import defines


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [TOCCommand]

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        action_gui_info = [
            ActionGUIInfo(GenerateTOC(self._application),
                          defines.MENU_TOC),
            ActionGUIInfo(InsertTOCCommand(self._application),
                          defines.MENU_TOC),
        ]

        new_menus = [(defines.MENU_TOC, _('Table of contents'), MENU_WIKI)]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info,
                                           new_menus=new_menus)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._destroy_guicontroller()

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды(:counter:)
        """
        list(map(lambda command: parser.addCommand(command(parser, self._application)),
                 self._commands))

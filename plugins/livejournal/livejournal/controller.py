# -*- coding: utf-8 -*-

import os.path

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo)

from .i18n import get_
from .ljcommand import LjUserCommand, LjCommunityCommand
from .actions import LJUserAction, LJCommAction
from . import defines


class Controller(object):
    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        self._actions_gui_controller = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        """
        Инициализация плагина
        """
        global _
        _ = get_()

        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(LJUserAction,
                          defines.MENU_LIVEJOURNAL,
                          defines.TOOLBAR_LIVEJOURNAL,
                          os.path.join(imagesPath, 'ljuser.gif')),
            ActionGUIInfo(LJCommAction,
                          defines.MENU_LIVEJOURNAL,
                          defines.TOOLBAR_LIVEJOURNAL,
                          os.path.join(imagesPath, 'ljcommunity.gif')),
        ]

        new_toolbars = [(defines.TOOLBAR_LIVEJOURNAL, _('LiveJournal'))]
        new_menus = [(defines.MENU_LIVEJOURNAL, _('LiveJournal'), MENU_WIKI_COMMANDS)]

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare

        if self._application.mainWindow is not None:
            self._actions_gui_controller.initialize(action_gui_info,
                                                    new_toolbars,
                                                    new_menus)

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        if self._application.mainWindow is not None:
            self._actions_gui_controller.destroy()

    def __onWikiParserPrepare(self, parser):
        """
        Добавление команд в википарсер
        """
        parser.addCommand(LjUserCommand(parser))
        parser.addCommand(LjCommunityCommand(parser))

# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.defines import TOOLBAR_PLUGINS
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .i18n import get_
from .commands import CommandOrg
from .actions import OrgAction


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [CommandOrg]

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
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(OrgAction(self._application),
                          MENU_WIKI_COMMANDS,
                          ButtonInfo(TOOLBAR_PLUGINS,
                                     os.path.join(imagesPath, 'org.png'))
                          ),
        ]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info)

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
        Вызывается до разбора викитекста. Добавление команды (:org:)
        """
        list(map(lambda command: parser.addCommand(command(parser)),
                 self._commands))

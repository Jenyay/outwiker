# -*- coding: utf-8 -*-

import os.path

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .i18n import get_
from .commands import CommandPlugin
from . import defines
from .actions import PluginAction


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
        self._commands = [CommandPlugin]

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
            ActionGUIInfo(PluginAction(self._application),
                          defines.MENU_PLUGINNAME,
                          ButtonInfo(defines.TOOLBAR_PLUGINNAME,
                                     os.path.join(imagesPath, 'button.png'))
                          ),
        ]

        new_toolbars = [(defines.TOOLBAR_PLUGINNAME, _('PluginName'))]
        new_menus = [(defines.MENU_PLUGINNAME, _('PluginName'), MENU_WIKI_COMMANDS)]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info,
                                           new_toolbars,
                                           new_menus)

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
        Вызывается до разбора викитекста. Добавление команд в википарсер
        """
        [*map(lambda command: parser.addCommand(command(parser)),
              self._commands)]

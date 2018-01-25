# -*- coding: utf-8 -*-

import os.path

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .i18n import get_
from .commands import PlotCommand
from . import defines
from .actions import PlotAction, OpenHelpAction


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__(self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [PlotCommand]

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
            ActionGUIInfo(PlotAction(self._application),
                          defines.MENU_DATAGRAPH,
                          ButtonInfo(defines.TOOLBAR_DATAGRAPH,
                                     os.path.join(imagesPath, 'plot.png'))
                          ),
            ActionGUIInfo(OpenHelpAction(self._application),
                          defines.MENU_DATAGRAPH,
                          ButtonInfo(defines.TOOLBAR_DATAGRAPH,
                                     os.path.join(imagesPath, 'help.png'))
                          ),
        ]

        new_toolbars = [(defines.TOOLBAR_DATAGRAPH, _('DataGraph'))]
        new_menus = [(defines.MENU_DATAGRAPH, _('DataGraph'), MENU_WIKI)]

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
        Вызывается до разбора викитекста. Добавление команды (:plot:)
        """
        [*map(lambda command: parser.addCommand(command(parser)),
              self._commands)]

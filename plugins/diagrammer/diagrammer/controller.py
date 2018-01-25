# -*- coding: utf-8 -*-

import os.path

from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)
from outwiker.pages.wiki.defines import MENU_WIKI
from outwiker.pages.wiki.wikipage import WikiWikiPage

from .i18n import get_
from .commanddiagram import CommandDiagram
from .diagramrender import DiagramRender
from . import defines

from .actions.insertdiagram import InsertDiagramAction
from .actions.help import HelpAction
from .actions.insertnode import InsertNodeAction
from .actions.insertgroup import InsertGroupAction
from .actions.insertedge import (InsertEdgeNoneAction,
                                 InsertEdgeRightAction,
                                 InsertEdgeLeftAction,
                                 InsertEdgeBothAction)


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
        self._commands = [CommandDiagram]

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

        DiagramRender.initialize()
        self._initialize_guicontroller()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare

    def _initialize_guicontroller(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(InsertDiagramAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'diagram.png'))
                          ),
            ActionGUIInfo(InsertNodeAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'node.png'))
                          ),
            ActionGUIInfo(InsertGroupAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'group.png'))
                          ),
            ActionGUIInfo(InsertEdgeNoneAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'edge-none.png'))
                          ),
            ActionGUIInfo(InsertEdgeLeftAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'edge-left.png'))
                          ),
            ActionGUIInfo(InsertEdgeRightAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'edge-right.png'))
                          ),
            ActionGUIInfo(InsertEdgeBothAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'edge-both.png'))
                          ),
            ActionGUIInfo(HelpAction(self._application),
                          defines.MENU_DIAGRAMMER,
                          ButtonInfo(defines.TOOLBAR_DIAGRAMMER,
                                     os.path.join(imagesPath, 'help.png'))
                          ),
        ]

        new_toolbars = [(defines.TOOLBAR_DIAGRAMMER, _('Diagrammer'))]
        new_menus = [(defines.MENU_DIAGRAMMER, _('Diagrammer'), MENU_WIKI)]

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
        Вызывается до разбора викитекста. Добавление команды(:counter:)
        """
        [*map(lambda command: parser.addCommand(command(parser)),
              self._commands)]

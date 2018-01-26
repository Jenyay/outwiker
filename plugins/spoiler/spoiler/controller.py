# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.defines import TOOLBAR_PLUGINS
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .commandspoiler import SpoilerCommand
from .actions import SpoilerAction


class Controller(object):
    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application
        self.__maxCommandIndex = 9

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        self._application.onWikiParserPrepare += self._onWikiParserPrepare
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(SpoilerAction(self._application),
                          MENU_WIKI_COMMANDS,
                          ButtonInfo(TOOLBAR_PLUGINS,
                                     os.path.join(imagesPath, 'spoiler.png'))
                          ),
        ]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info)

    def destroy(self):
        self._application.onWikiParserPrepare -= self._onWikiParserPrepare
        self._destroy_guicontroller()

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def _onWikiParserPrepare(self, parser):
        parser.addCommand(SpoilerCommand(parser, "spoiler", _))

        for index in range(self.__maxCommandIndex + 1):
            commandname = "spoiler{index}".format(index=index)
            parser.addCommand(SpoilerCommand(parser, commandname, _))

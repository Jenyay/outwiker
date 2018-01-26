# -*- coding: utf-8 -*-

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo)

from .stylecommand import StyleCommand
from .actions import StyleAction


class Controller(object):
    def __init__(self, application):
        self._application = application

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        self._application.onWikiParserPrepare += self._onWikiParserPrepare
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        action_gui_info = [
            ActionGUIInfo(StyleAction(self._application),
                          MENU_WIKI_COMMANDS
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
        parser.addCommand(StyleCommand(parser))

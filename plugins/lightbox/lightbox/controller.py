# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.defines import MENU_WIKI_COMMANDS, PAGE_TYPE_STRING
from outwiker.api.gui.actions import ActionsGUIController, ActionGUIInfo

from .lightboxcommand import LightboxCommand
from .actions import LightboxAction


class Controller:
    def __init__(self, application):
        self._application = application

        self._GUIController = ActionsGUIController(
            self._application,
            PAGE_TYPE_STRING,
        )

    def initialize(self):
        self._application.onWikiParserPrepare += self._onWikiParserPrepare
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        action_gui_info = [
            ActionGUIInfo(LightboxAction(self._application), MENU_WIKI_COMMANDS),
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
        parser.addCommand(LightboxCommand(parser))

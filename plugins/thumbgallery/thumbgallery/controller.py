# -*- coding: utf-8 -*-

import os.path

from outwiker.api.pages.wiki.defines import MENU_WIKI_COMMANDS, PAGE_TYPE_STRING
from outwiker.api.gui.defines import TOOLBAR_PLUGINS
from outwiker.api.gui.actions import ActionsGUIController, ActionGUIInfo, ButtonInfo

from .thumblistcommand import ThumbListCommand
from .thumbgallerycommand import ThumbGalleryCommand
from .actions import ThumbAction


class Controller:
    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        self._actions_gui_controller = ActionsGUIController(
            self._application,
            PAGE_TYPE_STRING,
        )

    def initialize(self):
        imagesPath = os.path.join(self._plugin.pluginPath, "images")

        action_gui_info = [
            ActionGUIInfo(
                ThumbAction(self._application),
                MENU_WIKI_COMMANDS,
                ButtonInfo(TOOLBAR_PLUGINS, os.path.join(imagesPath, "gallery.png")),
            ),
        ]

        self._application.onWikiParserPrepare += self._onWikiParserPrepare
        if self._application.mainWindow is not None:
            self._actions_gui_controller.initialize(action_gui_info)

    def destroy(self):
        self._application.onWikiParserPrepare -= self._onWikiParserPrepare
        if self._application.mainWindow is not None:
            self._actions_gui_controller.destroy()

    def _onWikiParserPrepare(self, parser):
        parser.addCommand(ThumbListCommand(parser))
        parser.addCommand(ThumbGalleryCommand(parser))

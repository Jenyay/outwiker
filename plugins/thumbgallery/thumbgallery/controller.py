# -*- coding: utf-8 -*-

import os.path

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.gui.defines import TOOLBAR_PLUGINS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .thumblistcommand import ThumbListCommand
from .thumbgallerycommand import ThumbGalleryCommand
from .actions import ThumbAction


class Controller(object):
    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        self._actions_gui_controller = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(ThumbAction(self._application),
                          MENU_WIKI_COMMANDS,
                          ButtonInfo(TOOLBAR_PLUGINS,
                                     os.path.join(imagesPath, 'gallery.png'))
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

# -*- coding: utf-8 -*-


import os.path

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.gui.defines import TOOLBAR_PLUGINS
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .actions import TexEquationAction
from .i18n import get_
from .preferencepanel import PreferencePanel
from .toolswindowcontroller import ToolsWindowController


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
        self._toolsWindowController = ToolsWindowController(self._application)

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._initialize_guicontroller()

        if self._application.mainWindow is not None:
            self._toolsWindowController.initialize()

    def _initialize_guicontroller(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(TexEquationAction(self._application),
                          MENU_WIKI_COMMANDS,
                          ButtonInfo(TOOLBAR_PLUGINS,
                                     os.path.join(imagesPath, 'equation.png'))
                          ),
        ]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._destroy_guicontroller()

        if self._application.mainWindow is not None:
            self._toolsWindowController.destroy()

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def __onWikiParserPrepare(self, parser):
        from .tokentex import TexFactory
        tex_inline = TexFactory().makeInlineTexToken(parser)
        tex_big = TexFactory().makeBigTexToken(parser)

        parser.wikiTokens.append(tex_big)
        parser.wikiTokens.append(tex_inline)

        parser.linkTokens.append(tex_big)
        parser.linkTokens.append(tex_inline)

        parser.headingTokens.append(tex_big)
        parser.headingTokens.append(tex_inline)

        parser.textLevelTokens.append(tex_big)
        parser.textLevelTokens.append(tex_inline)

        parser.listItemsTokens.append(tex_big)
        parser.listItemsTokens.append(tex_inline)

    def __onPreferencesDialogCreate(self, dialog):
        """
        Add page to preferences dialog
        """
        prefPanel = PreferencePanel(dialog.treeBook, self._application.config)

        panelName = _(u"TeXEquation [Plugin]")
        panelsList = [PreferencePanelInfo(prefPanel, panelName)]
        dialog.appendPreferenceGroup(panelName, panelsList)

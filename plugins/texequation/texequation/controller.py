# -*- coding: utf-8 -*-


import os.path

from outwiker.api.gui.defines import PREF_PANEL_PLUGINS
from outwiker.api.gui.defines import TOOLBAR_PLUGINS
from outwiker.api.pages.wiki import WikiWikiPage
from outwiker.api.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.api.gui.actions import ActionsGUIController, ActionGUIInfo, ButtonInfo

from .actions import TexEquationAction
from .i18n import get_
from .preferencepanel import PreferencePanel
from .toolswindowcontroller import ToolsWindowController


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
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

    def _get_image_full_path(self, fname):
        return os.path.join(self._plugin.pluginPath, "images", fname)

    def _initialize_guicontroller(self):
        action_gui_info = [
            ActionGUIInfo(
                TexEquationAction(self._application),
                MENU_WIKI_COMMANDS,
                ButtonInfo(TOOLBAR_PLUGINS, self._get_image_full_path("equation.svg")),
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
        dialog.addPage(
            prefPanel,
            _("TeXEquation [Plugin]"),
            parent_page_tag=PREF_PANEL_PLUGINS,
            icon_fname=self._get_image_full_path("equation.svg"),
        )

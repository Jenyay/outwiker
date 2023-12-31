# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki import WikiWikiPage
from outwiker.api.pages.wiki.defines import MENU_WIKI
from outwiker.api.gui.actions import ActionsGUIController, ActionGUIInfo
from outwiker.api.gui.defines import PREF_PANEL_PLUGINS

from .i18n import get_
from .menutoolscontroller import MenuToolsController
from .commandexec.commandcontroller import CommandController
from .commandexec.actions import (
    CommandExecAction,
    MacrosPageAction,
    MacrosHtmlAction,
    MacrosAttachAction,
    MacrosFolderAction,
)

from . import defines


class Controller:
    """
    Этот класс отвечает за основную работу плагина
    """

    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        self._page = None
        self._menuToolsController = MenuToolsController(self._application)
        self._commandController = CommandController(self._application)

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        global _
        _ = get_()

        self._menuToolsController.initialize()
        self._commandController.initialize()
        self._initialize_guicontroller()
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

    def _initialize_guicontroller(self):
        action_gui_info = [
            ActionGUIInfo(
                CommandExecAction(self._application), defines.MENU_EXTERNALTOOLS
            ),
            ActionGUIInfo(
                MacrosPageAction(self._application), defines.MENU_EXTERNALTOOLS
            ),
            ActionGUIInfo(
                MacrosHtmlAction(self._application), defines.MENU_EXTERNALTOOLS
            ),
            ActionGUIInfo(
                MacrosAttachAction(self._application), defines.MENU_EXTERNALTOOLS
            ),
            ActionGUIInfo(
                MacrosFolderAction(self._application), defines.MENU_EXTERNALTOOLS
            ),
        ]
        new_menus = [(defines.MENU_EXTERNALTOOLS, _("ExternalTools"), MENU_WIKI)]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info, new_menus=new_menus)

    def destroy(self):
        self._menuToolsController.destroy()
        self._commandController.destroy()
        self._destroy_guicontroller()
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def __onPreferencesDialogCreate(self, dialog):
        from .preferencespanel import PreferencesPanel

        prefPanel = PreferencesPanel(dialog.treeBook, self._application.config)
        dialog.addPage(prefPanel, _("External Tools [Plugin]"), parent_page_tag=PREF_PANEL_PLUGINS)

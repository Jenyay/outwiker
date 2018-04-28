# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.gui.defines import TOOLBAR_PLUGINS
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo,
                                                    ButtonInfo)

from .i18n import get_
from .preferencepanel import PreferencePanel
from .actions import InsertSourceAction


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """
        plugin - Владелец контроллера(экземпляр класса PluginSource)
        application - экземпляр класса ApplicationParams
        """
        self._plugin = plugin
        self._application = application

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

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(InsertSourceAction(self._application),
                          MENU_WIKI_COMMANDS,
                          ButtonInfo(TOOLBAR_PLUGINS,
                                     os.path.join(imagesPath, 'source.png'))
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

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды(:source:)
        """
        from .commandsource import CommandSource
        parser.addCommand(CommandSource(parser, self._application.config))

    def __onPreferencesDialogCreate(self, dialog):
        """
        Добавление страницы с настройками
        """
        prefPanel = PreferencePanel(dialog.treeBook, self._application.config)

        panelName = _(u"Source [Plugin]")
        panelsList = [PreferencePanelInfo(prefPanel, panelName)]
        dialog.appendPreferenceGroup(panelName, panelsList)

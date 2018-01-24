# -*- coding: utf-8 -*-

import os.path

import wx

import outwiker.core.exceptions
from outwiker.core.commands import testreadonly
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo)
from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
from outwiker.gui.defines import TOOLBAR_PLUGINS

from .i18n import get_
from .commandcounter import CommandCounter
from .insertdialog import InsertDialog
from .insertdialogcontroller import InsertDialogController
from .actions import InsertCounterAction


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
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        imagesPath = os.path.join(self._plugin.pluginPath, 'images')

        action_gui_info = [
            ActionGUIInfo(InsertCounterAction(self._application, self),
                          MENU_WIKI_COMMANDS,
                          TOOLBAR_PLUGINS,
                          os.path.join(imagesPath, 'counter.png')),
        ]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info)

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
        parser.addCommand(CommandCounter(parser))

    @testreadonly
    def insertCommand(self):
        """
        Вставка команды(:counter:) в редактор
        """
        if self._application.selectedPage.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        dlg = InsertDialog(self._application.mainWindow)

        dlgController = InsertDialogController(dlg,
                                               self._application.config,
                                               self._application.selectedPage)

        resultDlg = dlgController.showDialog()

        if resultDlg == wx.ID_OK:
            command = dlgController.getCommandString()
            self._getPageView().codeEditor.replaceText(command)

        dlg.Destroy()

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pageView

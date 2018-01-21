# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.core.commands import testreadonly
import outwiker.core.exceptions

from .i18n import get_
from .preferencepanel import PreferencePanel
from .insertdialog import InsertDialog
from .insertdialogcontroller import InsertDialogController
from .guicreator import GuiCreator


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

        self._guiCreator = None

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator(self, self._application)

        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

        if self._isWikiPage(self._application.selectedPage):
            self.__onPageViewCreate(self._application.selectedPage)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

        if self._isWikiPage(self._application.selectedPage):
            self._guiCreator.removeTools()

        self._guiCreator.destroy()

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

    def _isWikiPage(self, page):
        return page is not None and page.getTypeString() == u"wiki"

    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if self._isWikiPage(page):
            self._guiCreator.createTools()

    def __onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if self._isWikiPage(page):
            self._guiCreator.removeTools()

    @testreadonly
    def insertCommand(self):
        """
        Вставка команды(:source:) в редактор
        """
        if self._application.selectedPage.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        config = self._plugin.config

        dlg = InsertDialog(self._application.mainWindow)

        dlgController = InsertDialogController(self._application.selectedPage,
                                               dlg, config)
        resultDlg = dlgController.showDialog()

        if resultDlg == wx.ID_OK:
            command = dlgController.getCommandStrings()
            pageView = self._getPageView()
            pageView.codeEditor.turnText(command[0], command[1])

        dlg.Destroy()

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.core.commands import testreadonly
import outwiker.core.exceptions

from .i18n import get_
from .preferencepanel import PreferencePanel
from .insertdialog import InsertDialog
from .insertdialogcontroller import InsertDialogController
from .guicreators import OldGuiCreator, ActionGuiCreator


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        plugin - Владелец контроллера (экземпляр класса PluginSource)
        application - экземпляр класса ApplicationParams
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = None


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        # Создание класса для создания GUI в зависимости от того,
        # есть ли поддержка actions
        try:
            from outwiker.gui.baseaction import BaseAction
            self._guiCreator = ActionGuiCreator (self, self._application)
        except ImportError:
            self._guiCreator = OldGuiCreator (self, self._application)

        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self._guiCreator.removeTools()

        self._guiCreator.destroy ()


    def __onWikiParserPrepare (self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды (:source:)
        """
        from .commandsource import CommandSource
        parser.addCommand (CommandSource (parser, self._application.config))


    def __onPreferencesDialogCreate (self, dialog):
        """
        Добавление страницы с настройками
        """
        prefPanel = PreferencePanel (dialog.treeBook, self._application.config)

        panelName = _(u"Source [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)


    @property
    def _isCurrentWikiPage (self):
        """
        Возвращает True, если текущая страница - это викистраница, и False в противном случае
        """
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.createTools()


    def __onPageViewDestroy (self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.removeTools()


    @testreadonly
    def insertCommand (self):
        """
        Вставка команды (:source:) в редактор
        """
        if self._application.selectedPage.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        config = self._plugin.config

        dlg = InsertDialog (self._application.mainWindow)

        dlgController = InsertDialogController (self._application.selectedPage, dlg, config)
        resultDlg = dlgController.showDialog ()

        if resultDlg == wx.ID_OK:
            command = dlgController.getCommandStrings()
            pageView = self._getPageView()
            pageView.codeEditor.turnText (command[0], command[1])

        dlg.Destroy()


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

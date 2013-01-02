#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.core.system import getOS

from .i18n import get_
from .preferencepanel import PreferencePanel
from .insertdialog import InsertDialog
from .insertdialogcontroller import InsertDialogController


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        plugin - Владелец контроллера (экземпляр класса PluginSource)
        application - экземпляр класса ApplicationParams
        """
        self.SOURCE_TOOL_ID = u"PLUGIN_SOURCE_TOOL_ID"
        self._plugin = plugin
        self._application = application


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self._getPageView().removeTool (self.SOURCE_TOOL_ID)


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
        return (self._application.selectedPage != None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if page.getTypeString() != u"wiki":
            return

        pageView = self._getPageView()

        helpString = _(u"Source Code (:source ...:)")
        image = self._getImagePath ("source.png")

        pageView.addTool (pageView.commandsMenu, 
                self.SOURCE_TOOL_ID, 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                image)


    def __onInsertCommand (self, event):
        """
        Вставка команды (:source:) в редактор
        """
        config = self._plugin.config

        dlg = InsertDialog (self._application.mainWindow)

        dlgController = InsertDialogController (dlg, config)
        result = dlgController.showDialog ()

        dlg.Destroy()

        if result != None:
            startCommand = u'(:source lang="{language}" tabwidth={tabwidth}:)\n'.format (
                    language=config.defaultLanguage.value,
                    tabwidth=config.tabWidth.value
                    )

            endCommand = u'\n(:sourceend:)'

            pageView = self._getPageView()
            pageView.codeEditor.turnText (startCommand, endCommand)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView


    def _getImagePath (self, imageName):
        imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
        fname = os.path.join (imagedir, imageName)
        return fname

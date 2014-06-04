#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.commands import testreadonly
import outwiker.core.exceptions

from .i18n import get_
from .guicreator import GuiCreator
from .commandcounter import CommandCounter
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
        self._plugin = plugin
        self._application = application

        self._guiCreator = None


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self._guiCreator.removeTools()

        self._guiCreator.destroy ()


    def __onWikiParserPrepare (self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды (:counter:)
        """
        parser.addCommand (CommandCounter (parser))


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

        if page.getTypeString() == u"wiki":
            self._guiCreator.createTools()


    def __onPageViewDestroy (self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow != None

        if page.getTypeString() == u"wiki":
            self._guiCreator.removeTools()


    @testreadonly
    def insertCommand (self):
        """
        Вставка команды (:counter:) в редактор
        """
        if self._application.selectedPage.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        dlg = InsertDialog (self._application.mainWindow)

        dlgController = InsertDialogController (dlg, 
                self._application.config)

        resultDlg = dlgController.showDialog ()

        if resultDlg == wx.ID_OK:
            command = dlgController.getCommandString()
            self._getPageView().codeEditor.replaceText (command)

        dlg.Destroy()


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView



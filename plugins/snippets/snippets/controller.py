# -*- coding: UTF-8 -*-

import os

from outwiker.core.system import getSpecialDirList

from .i18n import get_
from .guicontroller import GuiController
from .defines import SNIPPETS_DIR
from snippets.actions.updatemenu import UpdateMenuAction
from snippets.actions.editsnippets import EditSnippetsAction
from snippets.actions.runrecentsnippet import RunRecentSnippet
from snippets.wikicommand import CommandSnip
from snippets.utils import getSnippetsDir


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__(self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiController = GuiController(application)

        self._actions = [
            (UpdateMenuAction, None),
            (EditSnippetsAction, None),
            (RunRecentSnippet, None),
        ]

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        snippets_dir_list = getSpecialDirList(SNIPPETS_DIR)
        assert len(snippets_dir_list) != 0
        if not os.path.exists(snippets_dir_list[-1]):
            os.mkdir(snippets_dir_list[-1])

        if self._application.mainWindow is not None:
            self._registerActions()
            self._guiController.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self.__onPageViewCreate(self._application.selectedPage)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        if self._application.mainWindow is not None:
            self._guiController.destroy()
            self._unregisterActions()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста.
        """
        command = CommandSnip(parser, getSnippetsDir(), self._application)
        parser.addCommand(command)

    @property
    def _isCurrentWikiPage(self):
        """
        Возвращает True, если текущая страница - это викистраница,
        и False в противном случае
        """
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")

    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

    def __onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

    def _registerActions(self):
        map(lambda actionTuple: self._application.actionController.register(
            actionTuple[0](self._application), actionTuple[1]), self._actions)

    def _unregisterActions(self):
        map(lambda actionTuple: self._application.actionController.removeAction(
            actionTuple[0].stringId), self._actions)

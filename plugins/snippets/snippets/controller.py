# -*- coding: utf-8 -*-

import os

from outwiker.core.system import getSpecialDirList

from .i18n import get_
from .guicontroller import GuiController
from .defines import SNIPPETS_DIR
from .actions.editsnippets import EditSnippetsAction
from .actions.runrecentsnippet import RunRecentSnippet
from .actions.openhelp import OpenHelpAction
from .wikicommand import CommandSnip
from .utils import getSnippetsDir


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
            (EditSnippetsAction, None),
            (RunRecentSnippet, None),
            (OpenHelpAction, None),
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

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

        if self._application.mainWindow is not None:
            self._guiController.destroy()
            self._unregisterActions()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста.
        """
        command = CommandSnip(parser, getSnippetsDir(), self._application)
        parser.addCommand(command)

    def _isWikiPage(self, page):
        return page is not None and page.getTypeString() == u"wiki"

    def _registerActions(self):
        [*map(lambda actionTuple: self._application.actionController.register(
            actionTuple[0](self._application), actionTuple[1]), self._actions)]

    def _unregisterActions(self):
        [*map(lambda actionTuple: self._application.actionController.removeAction(
            actionTuple[0].stringId), self._actions)]

# -*- coding: utf-8 -*-

from .i18n import get_
from .guicreator import GuiCreator
from .commands import CommandPlugin


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__(self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = GuiCreator(self, self._application)

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [CommandPlugin]

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isWikiPage(self._application.selectedPage):
            self.__onPageViewCreate(self._application.selectedPage)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        if self._isWikiPage(self._application.selectedPage):
            self._guiCreator.removeTools()

        self._guiCreator.destroy()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды (:counter:)
        """
        [*map(lambda command: parser.addCommand(command(parser)),
              self._commands)]

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

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

# -*- coding: UTF-8 -*-

from .i18n import get_
from .guicreator import GuiCreator
from .commands import CommandOrg


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = None

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [CommandOrg]


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
        list(map (lambda command: parser.addCommand (command (parser)), self._commands))


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


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

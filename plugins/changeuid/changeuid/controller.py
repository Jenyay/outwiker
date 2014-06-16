# -*- coding: UTF-8 -*-

from .i18n import get_
from .guicreator import GuiCreator


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


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()

        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        self._guiCreator.removeTools()
        self._guiCreator.destroy ()


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None
        self._guiCreator.createTools()


    def __onPageViewDestroy (self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None
        self._guiCreator.removeTools()

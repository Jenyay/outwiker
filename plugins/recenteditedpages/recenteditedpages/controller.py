# -*- coding: utf-8 -*-

from .i18n import get_


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        # self._application.onWikiParserPrepare += self.__onWikiParserPrepare

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        # self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        pass

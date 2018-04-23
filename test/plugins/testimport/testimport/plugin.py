# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

STRING = 'qqq'
INTEGER = 10
EXAMPLE_LIST = []


class TestImport(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self.__enabled = False

    @property
    def enabled(self):
        return self.__enabled

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return u"TestEmpty1"

    @property
    def description(self):
        return _(u"This plugin is empty")

    @property
    def version(self):
        return u"0.1"

    @version.setter
    def version(self, value):
        self._version = value

    def initialize(self):
        self.__enabled = True

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__enabled = False

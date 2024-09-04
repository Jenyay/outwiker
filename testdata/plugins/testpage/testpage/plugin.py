# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .testnotespage import TestPageFactory
from .testpageview import TestPageView


class PluginName(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "TestPage"

    @property
    def description(self):
        return _("Plugin description")

    @property
    def url(self):
        return _("http://jenyay.net")

    def initialize(self):
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    #############################################
    @property
    def TestPageFactory(self):
        return TestPageFactory

    @property
    def TestPageView(self):
        return TestPageView

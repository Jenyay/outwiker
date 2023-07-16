# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .i18n import set_
from .plugincontroller import PluginController


class PluginSessions(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self.__controller = PluginController(self, application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "Sessions"

    @property
    def description(self):
        return _("Save and restore tabs")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/SessionsEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

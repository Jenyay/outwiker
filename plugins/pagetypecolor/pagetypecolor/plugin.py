# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .i18n import set_
from .controller import Controller


class PluginPageTypeColor(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "PageTypeColor"

    @property
    def description(self):
        return _(
            "Plugin colorize the page dialog controls in depending on the selected page type."
        )

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/PageTypeColorEn")

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

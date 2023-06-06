# -*- coding: utf-8 -*-

import os.path

from outwiker.api.core.plugins import Plugin

from .i18n import set_


from .controller import Controller


class PluginWebPage(Plugin):
    def __init__(self, application):
        """
        application - instance of the core.application.ApplicationParams
        class
        """
        super().__init__(application)
        self.__controller = Controller(self, self._application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################
    @property
    def name(self):
        return "WebPage"

    @property
    def description(self):
        return _("Plug-in for downloading HTML pages from web")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/WebPageEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от
        всех событий
        """
        self.__controller.destroy()

# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginExport2Html (Plugin):
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
        return u"Export2Html"

    @property
    def description(self):
        return _(u"Export pages to HTML")

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

    #############################################

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/Export2HtmlPluginEn")

# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .i18n import set_
from .controller import Controller


class PluginDataGraph(Plugin):
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
        return "DataGraph"

    @property
    def description(self):
        return _("DataGraph plug-in designed for creation a charts by text data.")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/DataGraphEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        self.__controller.destroy()

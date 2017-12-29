# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

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
        return u"DataGraph"

    @property
    def description(self):
        return _(u"DataGraph plug-in designed for creation a charts by text data.")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/DataGraphEn")

    def initialize(self):
        if self._application.mainWindow is not None:
            self._initlocale(u"datagraph")

        self.__controller.initialize()

    def destroy(self):
        self.__controller.destroy()

    #############################################

    def _initlocale(self, domain):
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException as e:
            print(e)

        set_(_)

# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version
from outwiker.core.system import getOS


if getCurrentVersion() < Version (1, 8, 0, 750):
    print ("DataGraph plugin. OutWiker version requirement: 1.8.0.750")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginDataGraph (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"DataGraph"


        @property
        def description (self):
            return _(u"Plugin description")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net")


        def initialize(self):
            if self._application.mainWindow is not None:
                self._initlocale(u"datagraph")
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_(_)


        @property
        def PlotCommand (self):
            from commands import PlotCommand
            return PlotCommand


        @property
        def GraphBuilder (self):
            from graphbuilder import GraphBuilder
            return GraphBuilder

# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet


if getCurrentVersion() < Version (1, 8, 0, 733, status=StatusSet.BETA):
    print ("TestPage plugin. OutWiker version requirement: 1.8.0.733")
else:
    from .controller import Controller

    class PluginLatexPage (Plugin):
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
            return u"LatexPage"


        @property
        def description (self):
            return _(u"Plugin description")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"https://jenyay.net")


        def initialize(self):
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

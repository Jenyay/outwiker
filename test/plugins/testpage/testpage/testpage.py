# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller
from .testnotespage import TestPage, TestPageFactory
from .testpageview import TestPageView


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    print ("TestPage plugin. OutWiker version requirement: 2.1.0.833")
else:
    class PluginName (Plugin):
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
            return u"TestPage"


        @property
        def description (self):
            return _(u"Plugin description")


        @property
        def version (self):
            return u"2.0"


        @property
        def url (self):
            return _(u"http://jenyay.net")


        def initialize(self):
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        @property
        def TestPage (self):
            return TestPage


        @property
        def TestPageFactory (self):
            return TestPageFactory


        @property
        def TestPageView (self):
            return TestPageView

# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller

__version__ = u'1.0'


if getCurrentVersion() < Version (1, 9, 0, 781, status=StatusSet.DEV):
    print ("WebPage plugin. OutWiker version requirement: 1.9.0.781")
else:
    class PluginWebPage (Plugin):
        def __init__ (self, application):
            """
            application - instance of the core.application.ApplicationParams class
            """
            super (PluginWebPage, self).__init__ (application)
            self.__controller = Controller(self, self._application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################
        @property
        def name (self):
            return u"WebPage"


        @property
        def description (self):
            return _(u"Download HTML pages from web")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/WebPageEn")


        def initialize(self):
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

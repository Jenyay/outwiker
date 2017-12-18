# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


__version__ = u'2.0'


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    logging.warning ("PluginName plugin. OutWiker version requirement: 2.1.0.833")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginOrganizer (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super (PluginOrganizer, self).__init__ (application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Organizer"


        @property
        def description (self):
            return _(u"Plugin description")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net")


        def initialize(self):
            self._initlocale(u"organizer")
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = os.path.join (os.path.dirname (__file__), "locale")
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print (e)

            set_(_)

# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


__version__ = u'1.0'


if getCurrentVersion() < Version (1, 9, 0, 777, status=StatusSet.DEV):
    logging.warning ("PluginName plugin. OutWiker version requirement: 1.9.0.777")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginPageTypeColor (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super (PluginPageTypeColor, self).__init__ (application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"PageTypeColor"


        @property
        def description (self):
            return _(u"Plugin colorize the page dialog controls in depending on the selected page type.")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/PageTypeColorEn")


        def initialize(self):
            self._initlocale(u"pagetypecolor")
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__),
                                             "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_(_)

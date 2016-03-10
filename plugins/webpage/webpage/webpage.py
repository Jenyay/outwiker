# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_


__version__ = u'1.0.1'


if getCurrentVersion() < Version (1, 9, 0, 781, status=StatusSet.DEV):
    logging.warning (u"WebPage plugin. OutWiker version requirement: 1.9.0.781")
else:
    from .controller import Controller

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
            self._initlocale(u'webpage')
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
            except BaseException:
                pass

            set_(_)

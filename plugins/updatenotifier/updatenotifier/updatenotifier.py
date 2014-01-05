#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_
from .versionextractor import extractVersion
from .versionlist import VersionList
from .controller import Controller


if getCurrentVersion() < Version (1, 7, 0, 684, status=StatusSet.DEV):
    print ("Spoiler plugin. OutWiker version requirement: 1.7.0.684")
else:
    class PluginUpdateNotifier (Plugin):
        """
        Класс плагина для слежения за появлением новых версий программы и плагинов
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self._controller = Controller(application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"UpdateNotifier"

        
        @property
        def description (self):
            return _(u'''Check for update OutWiker and plug-ins for it. Append menu item "Help -> Check for Updates..."''')


        @property
        def version (self):
            return u"1.1"


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/UpdateNotifierEn")
        
        
        def initialize(self):
            self._initlocale(u"updatenotifier")
            self._controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)


        @property
        def extractVersion (self):
            return extractVersion


        @property
        def VersionList (self):
            return VersionList


        @property
        def loaders (self):
            import loaders
            return loaders

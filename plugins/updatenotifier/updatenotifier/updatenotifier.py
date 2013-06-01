#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_


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
            return _(u"Plugin description")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net")
        
        
        def initialize(self):
            self._initlocale(u"updatenotifier")


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            pass

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)

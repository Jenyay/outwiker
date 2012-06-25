#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller


# Для работы этого плагина требуется OutWiker 1.6.0.632
if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
    print ("Thumblist plugin. OutWiker version requirement: 1.6.0.632")
else:
    class PluginThumbGallery (Plugin):
        """
        Плагин, добавляющий обработку команды (:thumblist:) и (:thumbgallery:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self._controller = Controller (application)


        @property
        def name (self):
            return u"ThumbGallery"

        
        @property
        def description (self):
            return _(u"""Add command (:thumblist:) to wiki parser.""")


        @property
        def version (self):
            return u"1.0"


        def initialize(self):
            self._initlocale(u"thumblist")
            self._controller.initialize()


        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._controller.destroy()

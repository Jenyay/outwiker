# -*- coding: UTF-8 -*-

import os
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_


if getCurrentVersion() < Version (2, 0, 0, 801, status=StatusSet.DEV):
    print ("Markdown plugin. OutWiker version requirement: 2.0.0.801")
else:
    class PluginMarkdown (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self._correctSysPath()

            from .controller import Controller
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Markdown"


        @property
        def description (self):
            return _(u"The Markdown plug-in add a new page type with Markdown notation")


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/MarkdownEn")


        def initialize(self):
            self._initlocale(u'markdown')
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.clear()

        #############################################

        def _correctSysPath (self):
            syspath = [unicode (item, getOS().filesEncoding)
                       if not isinstance (item, unicode)
                       else item for item in sys.path]

            if self._pluginPath not in syspath:
                sys.path.insert(0, self._pluginPath)

        def _initlocale (self, domain):
            langdir = os.path.join(self._pluginPath, "locale")
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException:
                pass

            set_(_)

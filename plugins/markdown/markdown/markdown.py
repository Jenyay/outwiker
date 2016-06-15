# -*- coding: UTF-8 -*-

import os
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version
from outwiker.core.system import getOS


if getCurrentVersion() < Version (1, 9, 0, 790):
    print ("Markdown plugin. OutWiker version requirement: 1.9.0.790")
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
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/MarkdownEn")


        def initialize(self):
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.clear()

        #############################################

        def _correctSysPath (self):
            currentpath = os.path.dirname(os.path.abspath(__file__))
            currentpath = unicode (currentpath, getOS().filesEncoding)

            syspath = [unicode (item, getOS().filesEncoding)
                       if not isinstance (item, unicode)
                       else item for item in sys.path]

            if currentpath not in syspath:
                sys.path.insert(0, currentpath)

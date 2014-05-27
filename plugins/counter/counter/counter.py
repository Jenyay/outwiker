#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .commandcounter import CommandCounter

# Для работы этого плагина требуется OutWiker 1.8.0.720
if getCurrentVersion() < Version (1, 8, 0, 720, status=StatusSet.DEV):
    print ("Style plugin. OutWiker version requirement: 1.8.0.720")
else:
    class PluginTestWikiCommand (Plugin):
        """
        Плагин, добавляющий обработку команды TestCommand в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)


        def __onWikiParserPrepare (self, parser):
            parser.addCommand (CommandCounter (parser))


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Counter"

        
        @property
        def description (self):
            return u"Add command (:counter:) in wiki parser"


        @property
        def version (self):
            return u"1.0"


        def initialize(self):
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

        #############################################

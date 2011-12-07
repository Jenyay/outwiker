#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin

from .commandcounter import CommandCounter


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
        return u"CounterWikiCommand"

    
    @property
    def description (self):
        return u"Add command (:counter:) in wiki parser"


    @property
    def version (self):
        return u"0.1"


    def initialize(self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    #############################################

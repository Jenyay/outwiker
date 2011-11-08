#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin


class PluginSourceCommand (Plugin):
    """
    Плагин, добавляющий обработку команды (:source:) в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)

    
    def __onWikiParserPrepare (self, parser):
        from .commandsource import CommandSource
        parser.addCommand (CommandSource (parser))


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name (self):
        return u"Source"

    
    @property
    def description (self):
        return _(u"""Add command (:source:) in wiki parser. This command highlight your source code.

<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)

<B>Params:</B>
<I>lang</I> - programming language
<I>tabwidth</I> - tab size

<B>Example:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>
""")


    @property
    def version (self):
        return u"1.0"


    def __initlocale (self):
        domain = u"source"

        langdir = os.path.join (os.path.dirname (__file__), "locale")
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e



    def initialize(self):
        self.__initlocale()

        cmd_folder = os.path.dirname(os.path.abspath(__file__))
        if cmd_folder not in sys.path:
            sys.path.insert(0, cmd_folder)

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    #############################################

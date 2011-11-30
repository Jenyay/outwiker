#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS

from .stylecommand import StyleCommand


class PluginStyle (Plugin):
    """
    Плагин, добавляющий обработку команды (:style:) в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)


    def __onWikiParserPrepare (self, parser):
        parser.addCommand (StyleCommand (parser))


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name (self):
        return u"Style"

    
    @property
    def description (self):
        return _(u"""Add command (:style:) to wiki parser. This command allow the setting of a user CSS style for a page.

<B>Usage</B>:
(:style:)
styles
(:styleend:)

<B>Example:</B>
(:style:)
body {background-color: #EEE;}
(:styleend:)
""")


    @property
    def version (self):
        return u"1.0"


    def initialize(self):
        domain = u"style"

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e
            # raise

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    #############################################

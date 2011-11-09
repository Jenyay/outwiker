#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.pages.wiki.wikipanel import WikiPagePanel


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


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if page.getTypeString() != u"wiki":
            return

        pageView = self._application.mainWindow.pagePanel.pageView
        assert type (pageView) == WikiPagePanel

        pageView.addTool (pageView.commandsMenu, 
                "ID_SOURCE", 
                lambda event: pageView.codeEditor.turnText (u'(:source lang="" tabwidth=4:)\n', u'\n(:sourceend:)'), 
                _(u"Source Code (:source ...:)"), 
                _(u"Source Code (:source ...:)"), 
                None)


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
        return u"1.1"


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
        self._application.onPageViewCreate += self.__onPageViewCreate




    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate

    #############################################

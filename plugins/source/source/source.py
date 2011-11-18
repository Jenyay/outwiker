#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.pages.wiki.wikipanel import WikiPagePanel
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .sourceconfig import SourceConfig


class PluginSource (Plugin):
    """
    Плагин, добавляющий обработку команды (:source:) в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)
        self.__version = u"1.2.1"


    def initialize(self):
        self.__initlocale()

        cmd_folder = os.path.dirname(os.path.abspath(__file__))
        if cmd_folder not in sys.path:
            sys.path.insert(0, cmd_folder)

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

    
    def __onWikiParserPrepare (self, parser):
        from .commandsource import CommandSource
        parser.addCommand (CommandSource (parser, self._application.config))


    def __onPreferencesDialogCreate (self, dialog):
        from .preferencepanel import PreferencePanel
        prefPanel = PreferencePanel (dialog.treeBook, self._application.config, _)

        panelName = _(u"Source [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if page.getTypeString() != u"wiki":
            return

        pageView = self.__getPageView()

        helpString = _(u"Source Code (:source ...:)")
        pageView.addTool (pageView.commandsMenu, 
                "ID_PLUGIN_SOURCE", 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                None)


    def __getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        pageView = self._application.mainWindow.pagePanel.pageView
        assert type (pageView) == WikiPagePanel

        return pageView


    @property
    def config (self):
        return SourceConfig (self._application.config)


    def __onInsertCommand (self, event):
        config = self.config

        startCommand = u'(:source lang="{language}" tabwidth={tabwidth}:)\n'.format (
                language=config.defaultLanguage.value,
                tabwidth=config.tabWidth.value
                )

        endCommand = u'\n(:sourceend:)'

        pageView = self.__getPageView()
        pageView.codeEditor.turnText (startCommand, endCommand)


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
        return self.__version


    def __initlocale (self):
        domain = u"source"

        langdir = os.path.join (os.path.dirname (__file__), "locale")
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate

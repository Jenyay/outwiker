#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .ljcommand import LjUserCommand, LjCommunityCommand


# Для работы этого плагина требуется версия OutWiker 1.6.0.632
if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
    print ("Livejournal plugin. OutWiker version requirement: 1.6.0.632")
else:
    class PluginLivejournal (Plugin):
        """
        Плагин, добавляющий обработку команды spoiler в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.ID_LJUSER = u"PLUGIN_LIVEJOURNAL_LJUSER_ID"
            self.ID_LJCOMMUNITY = u"PLUGIN_LIVEJOURNAL_LJCOMMUNITY_ID"


        def __onWikiParserPrepare (self, parser):
            parser.addCommand (LjUserCommand (parser))
            parser.addCommand (LjCommunityCommand (parser))


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        def initialize(self):
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageViewCreate += self.__onPageViewCreate
            self.__initlocale()

            if self._isCurrentWikiPage:
                self.__onPageViewCreate (self._application.selectedPage)


        def __initlocale (self):
            domain = u"livejournal"

            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e
            pass


        @property
        def _isCurrentWikiPage (self):
            return (self._application.selectedPage != None and
                    self._application.selectedPage.getTypeString() == u"wiki")


        def __onPageViewCreate(self, page):
            """Обработка события после создания представления страницы"""
            assert self._application.mainWindow != None

            if not self._isCurrentWikiPage:
                return

            pageView = self.__getPageView()

            pageView.addTool (pageView.commandsMenu, 
                    self.ID_LJUSER, 
                    lambda event: pageView.codeEditor.turnText (u"(:ljuser ", u":)"), 
                    _(u"Livejournal User (:ljuser ...:)"), 
                    _(u"Livejournal User (:ljuser ...:)"), 
                    self.__getButtonImage ("ljuser.gif"),
                    False)

            pageView.addTool (pageView.commandsMenu, 
                    self.ID_LJCOMMUNITY, 
                    lambda event: pageView.codeEditor.turnText (u"(:ljcomm ", u":)"), 
                    _(u"Livejournal Community (:ljcomm ...:)"), 
                    _(u"Livejournal Community (:ljcomm ...:)"), 
                    self.__getButtonImage ("ljcommunity.gif"),
                    False)

            
        def __getButtonImage (self, fname):
            imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
            return os.path.join (imagedir, fname)


        def __getPageView (self):
            """
            Получить указатель на панель представления страницы
            """
            pageView = self._application.mainWindow.pagePanel.pageView
            assert type (pageView) == WikiPagePanel

            return pageView


        @property
        def name (self):
            return u"Livejournal"

        
        @property
        def description (self):
            return _(u"""Add commands (:ljuser:) and (:ljcomm:) in wiki parser.

    <B>Usage:</B>
    (:ljuser username:)
    (:ljcomm communityname:)
    """)


        @property
        def version (self):
            return u"1.0"


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onPageViewCreate -= self.__onPageViewCreate

            if self._isCurrentWikiPage:
                self.__getPageView().removeTool (self.ID_LJUSER)
                self.__getPageView().removeTool (self.ID_LJCOMMUNITY)

        #############################################

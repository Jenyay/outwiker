#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .lightboxcommand import LightboxCommand


# Для работы этого плагина требуется OutWiker 1.6.0.632 и выше
if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
    print ("Style plugin. OutWiker version requirement: 1.6.0.632")
else:
    class PluginLightbox (Plugin):
        """
        Плагин, добавляющий обработку команды (:lightbox:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.LIGHTBOX_TOOL_ID = u"PLUGIN_LIGHTBOX_TOOL_ID"


        def __onWikiParserPrepare (self, parser):
            parser.addCommand (LightboxCommand (parser))
            pass


        @property
        def name (self):
            return u"Lightbox"

        
        @property
        def description (self):
            return _(u"""Add command (:lightbox:) to wiki parser.""")


        @property
        def version (self):
            return u"1.0"


        def initialize(self):
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageViewCreate += self.__onPageViewCreate
            self._initlocale(u"lightbox")

            if self._isCurrentWikiPage:
                self.__onPageViewCreate (self._application.selectedPage)


        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e


        def __onPageViewCreate(self, page):
            """Обработка события после создания представления страницы"""
            assert self._application.mainWindow != None

            if not self._isCurrentWikiPage:
                return

            pageView = self._getPageView()

            helpString = _(u"Use lightbox (:lightbox:)")

            pageView.addTool (pageView.commandsMenu, 
                    self.LIGHTBOX_TOOL_ID, 
                    self.__onInsertCommand, 
                    helpString, 
                    helpString, 
                    None)
            

        def __onInsertCommand (self, event):
            command = u'(:lightbox:)'

            pageView = self._getPageView()
            pageView.codeEditor.replaceText (command)


        def _getPageView (self):
            """
            Получить указатель на панель представления страницы
            """
            return self._application.mainWindow.pagePanel.pageView


        @property
        def _isCurrentWikiPage (self):
            return (self._application.selectedPage != None and
                    self._application.selectedPage.getTypeString() == u"wiki")


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onPageViewCreate -= self.__onPageViewCreate

            if self._isCurrentWikiPage:
                self._getPageView().removeTool (self.LIGHTBOX_TOOL_ID)

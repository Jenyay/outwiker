#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .thumblistcommand import ThumbListCommand
from .thumbgallerycommand import ThumbGalleryCommand


# Для работы этого плагина требуется OutWiker 1.6.0.632
if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
    print ("Thumblist plugin. OutWiker version requirement: 1.6.0.632")
else:
    class PluginThumbList (Plugin):
        """
        Плагин, добавляющий обработку команды (:thumblist:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.THUMBLIST_TOOL_ID = u"PLUGIN_THUMBLIST_TOOL_ID"


        def __onWikiParserPrepare (self, parser):
            parser.addCommand (ThumbListCommand (parser))
            parser.addCommand (ThumbGalleryCommand (parser))


        @property
        def name (self):
            return u"ThumbList"

        
        @property
        def description (self):
            return _(u"""Add command (:thumblist:) to wiki parser.""")


        @property
        def version (self):
            return u"1.0"


        def initialize(self):
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageViewCreate += self.__onPageViewCreate
            self._initlocale(u"thumblist")

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

            helpString = _(u"Thumbnails Gallery (:thumbgallery:)")

            pageView.addTool (pageView.commandsMenu, 
                    self.THUMBLIST_TOOL_ID, 
                    self.__onInsertCommand, 
                    helpString, 
                    helpString, 
                    self._getImagePath (u"gallery.png"),
                    False)
            

        def __onInsertCommand (self, event):
            startCommand = u'(:thumbgallery:)\n'
            endCommand = u'\n(:thumbgalleryend:)'

            pageView = self._getPageView()
            pageView.codeEditor.turnText (startCommand, endCommand)


        def _getPageView (self):
            """
            Получить указатель на панель представления страницы
            """
            return self._application.mainWindow.pagePanel.pageView


        def _getImagePath (self, fname):
            imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), 
                    getOS().filesEncoding)
            return os.path.join (imagedir, fname)


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
                self._getPageView().removeTool (self.THUMBLIST_TOOL_ID)

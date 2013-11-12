#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .ljcommand import LjUserCommand, LjCommunityCommand
from .ljtoolbar import LJToolBar


# Для работы этого плагина требуется версия OutWiker 1.7.0.670
if getCurrentVersion() < Version (1, 7, 0, 670, status=StatusSet.DEV):
    print ("Livejournal plugin. OutWiker version requirement: 1.7.0.670")
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
            self.ID_TOOLBAR = u"livejournal"
            self.ID_LJUSER = u"PLUGIN_LIVEJOURNAL_LJUSER_ID"
            self.ID_LJCOMMUNITY = u"PLUGIN_LIVEJOURNAL_LJCOMMUNITY_ID"

            self.__toolbarCreated = False


        def __onWikiParserPrepare (self, parser):
            """
            Добавление команд в википарсер
            """
            parser.addCommand (LjUserCommand (parser))
            parser.addCommand (LjCommunityCommand (parser))


        def initialize(self):
            """
            Инициализация плагина
            """
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageViewCreate += self.__onPageViewCreate
            self._application.onPageViewDestroy += self.__onPageViewDestroy
            self._initlocale("livejournal")

            if self._isCurrentWikiPage:
                self.__onPageViewCreate (self._application.selectedPage)


        def _initlocale (self, domain):
            """
            Загрузить перевод
            """
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e


        def __onPageViewDestroy (self, page):
            """
            Обработчик события выбора новой страницы
            """
            self.__destroyToolBar()


        @property
        def _isCurrentWikiPage (self):
            """
            Возвращает True, если текущая страница - это викистраница
            """
            return (self._application.selectedPage != None and
                    self._application.selectedPage.getTypeString() == u"wiki")


        def __createToolBar (self):
            """
            Создание панели с кнопками, если она еще не была создана
            """
            if not self.__toolbarCreated:
                mainWnd = self._application.mainWindow
                mainWnd.toolbars[self.ID_TOOLBAR] = LJToolBar (mainWnd, mainWnd.auiManager)

                pageView = self._getPageView()
                pageView.addTool (pageView.commandsMenu, 
                        self.ID_LJUSER, 
                        self.__turnLJUser, 
                        _(u"Livejournal User (:ljuser ...:)"), 
                        _(u"Livejournal User (:ljuser ...:)"), 
                        self._getImagePath ("ljuser.gif"),
                        False,
                        panelname=self.ID_TOOLBAR)

                pageView.addTool (pageView.commandsMenu, 
                        self.ID_LJCOMMUNITY, 
                        self.__turnLJCommunity, 
                        _(u"Livejournal Community (:ljcomm ...:)"), 
                        _(u"Livejournal Community (:ljcomm ...:)"), 
                        self._getImagePath ("ljcommunity.gif"),
                        False,
                        panelname=self.ID_TOOLBAR)

                self.__toolbarCreated = True


        def __turnLJUser (self, event):
            """
            Обработчик нажатия кнопки для вставки ЖЖ-пользователя
            """
            pageView = self._getPageView()
            pageView.codeEditor.turnText (u"(:ljuser ", u":)")


        def __turnLJCommunity (self, event):
            """
            Обработчик нажатия кнопки для вставки ЖЖ-сообщества
            """
            pageView = self._getPageView()
            pageView.codeEditor.turnText (u"(:ljcomm ", u":)")


        def __destroyToolBar (self):
            """
            Уничтожение панели с кнопками
            """
            if self.__toolbarCreated:
                self._application.mainWindow.toolbars.destroyToolBar (self.ID_TOOLBAR)
                self.__toolbarCreated = False


        def __onPageViewCreate(self, page):
            """Обработка события после создания представления страницы"""
            assert self._application.mainWindow != None

            if not self._isCurrentWikiPage:
                self.__destroyToolBar()
                return

            self.__createToolBar()


        def _getImagePath (self, fname):
            imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
            return os.path.join (imagedir, fname)


        def _getPageView (self):
            """
            Получить указатель на панель представления страницы
            """
            return self._application.mainWindow.pagePanel.pageView


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
            return u"1.2.1"


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onPageViewCreate -= self.__onPageViewCreate
            self._application.onPageViewDestroy -= self.__onPageViewDestroy

            self.__destroyToolBar()

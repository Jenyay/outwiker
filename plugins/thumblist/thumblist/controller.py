#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.system import getOS
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .thumblistcommand import ThumbListCommand
from .thumbgallerycommand import ThumbGalleryCommand


class Controller (object):
    """
    Основные действия плагина собраны в этом классе
    """
    def __init__ (self, application):
        self.THUMBLIST_TOOL_ID = u"PLUGIN_THUMBLIST_TOOL_ID"
        self._application = application        

        
    def __onWikiParserPrepare (self, parser):
        parser.addCommand (ThumbListCommand (parser))
        parser.addCommand (ThumbGalleryCommand (parser))


    def initialize (self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate

        if self._isCurrentWikiPage:
            self._getPageView().removeTool (self.THUMBLIST_TOOL_ID)


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


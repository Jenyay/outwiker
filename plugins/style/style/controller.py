# -*- coding: utf-8 -*-

from .stylecommand import StyleCommand
from .guicreator import GuiCreator


class Controller(object):
    def __init__(self, application):
        self._application = application
        self.STYLE_TOOL_ID = u"PLUGIN_STYLE_TOOL_ID"
        self._guiCreator = GuiCreator(self._application)

    def initialize(self):
        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self.__onPageViewCreate(self._application.selectedPage)

    def destroy(self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self._guiCreator.removeTools()

        self._guiCreator.destroy()

    def __onWikiParserPrepare(self, parser):
        parser.addCommand(StyleCommand(parser))

    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.createTools()

    def __onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.removeTools()

    @property
    def _isCurrentWikiPage(self):
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")

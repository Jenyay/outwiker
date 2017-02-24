# -*- coding: UTF-8 -*-

from .i18n import get_
from .guicreator import GuiCreator


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = None


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self._guiCreator.removeTools()

        self._guiCreator.destroy ()


    def __onWikiParserPrepare (self, parser):
        from tokentex import TexFactory
        tex_inline = TexFactory().makeInlineTexToken (parser)
        tex_big = TexFactory().makeBigTexToken (parser)

        parser.wikiTokens.append (tex_big)
        parser.wikiTokens.append (tex_inline)

        parser.linkTokens.append (tex_big)
        parser.linkTokens.append (tex_inline)

        parser.headingTokens.append (tex_big)
        parser.headingTokens.append (tex_inline)

        parser.textLevelTokens.append (tex_big)
        parser.textLevelTokens.append (tex_inline)

        parser.listItemsTokens.append (tex_big)
        parser.listItemsTokens.append (tex_inline)


    @property
    def _isCurrentWikiPage (self):
        """
        Возвращает True, если текущая страница - это викистраница, и False в противном случае
        """
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.createTools()


    def __onPageViewDestroy (self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.removeTools()


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

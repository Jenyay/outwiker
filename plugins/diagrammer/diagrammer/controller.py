# -*- coding: UTF-8 -*-

from .i18n import get_
from .guicreator import GuiCreator
from .commanddiagram import CommandDiagram


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

        # В этот список добавить новые викикоманды, если они нужны
        self._commands = [CommandDiagram]


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self.__initBlockdiag()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def __initBlockdiag (self):
        import blockdiag.noderenderer.actor
        import blockdiag.noderenderer.beginpoint
        import blockdiag.noderenderer.box
        import blockdiag.noderenderer.circle
        import blockdiag.noderenderer.cloud
        import blockdiag.noderenderer.diamond
        import blockdiag.noderenderer.dots
        import blockdiag.noderenderer.ellipse
        import blockdiag.noderenderer.endpoint
        import blockdiag.noderenderer.mail
        import blockdiag.noderenderer.minidiamond
        import blockdiag.noderenderer.none
        import blockdiag.noderenderer.roundedbox
        import blockdiag.noderenderer.square
        import blockdiag.noderenderer.textbox

        from blockdiag.imagedraw.png import setup

        setup(None)
        # init_imagedrawers()
        # init_renderers()
        # imagedraw.init_imagedrawers()
        # imagedraw.create("png", fname, debug=True)
        blockdiag.noderenderer.actor.setup(None)
        blockdiag.noderenderer.beginpoint.setup(None)
        blockdiag.noderenderer.box.setup(None)
        blockdiag.noderenderer.circle.setup(None)
        blockdiag.noderenderer.cloud.setup(None)
        blockdiag.noderenderer.diamond.setup(None)
        blockdiag.noderenderer.dots.setup(None)
        blockdiag.noderenderer.ellipse.setup(None)
        blockdiag.noderenderer.endpoint.setup(None)
        blockdiag.noderenderer.mail.setup(None)
        blockdiag.noderenderer.minidiamond.setup(None)
        blockdiag.noderenderer.none.setup(None)
        blockdiag.noderenderer.roundedbox.setup(None)
        blockdiag.noderenderer.square.setup(None)
        blockdiag.noderenderer.textbox.setup(None)


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
        """
        Вызывается до разбора викитекста. Добавление команды (:counter:)
        """
        map (lambda command: parser.addCommand (command (parser)), self._commands)


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

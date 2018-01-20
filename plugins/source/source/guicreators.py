# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from outwiker.gui.defines import TOOLBAR_PLUGINS

from .misc import getImagePath
from .i18n import get_


class BaseGuiCreator(object, metaclass=ABCMeta):
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

    def initialize(self):
        global _
        _ = get_()

    @abstractmethod
    def createTools(self):
        pass

    @abstractmethod
    def removeTools(self):
        pass

    @abstractmethod
    def destroy(self):
        pass


class ActionGuiCreator(BaseGuiCreator):
    """
    Создание элементов интерфейса с использованием actions
    """
    def initialize(self):
        super(ActionGuiCreator, self).initialize()
        from .actions import InsertSourceAction

        if self._application.mainWindow is not None:
            self._application.actionController.register(
                InsertSourceAction(self._application, self._controller),
                None)

    def createTools(self):
        from .actions import InsertSourceAction

        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        toolbar = mainWindow.toolbars[TOOLBAR_PLUGINS]

        pageView = self._getPageView()

        self._application.actionController.appendMenuItem(
            InsertSourceAction.stringId,
            pageView.commandsMenu)

        self._application.actionController.appendToolbarButton(
            InsertSourceAction.stringId,
            toolbar,
            getImagePath("source.png"))

        try:
            # Это событие появилось только в версии 1.8.0.717
            from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
            pageView.Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
            self._enableTools()
        except ImportError:
            pass

    def removeTools(self):
        from .actions import InsertSourceAction

        self._application.actionController.removeMenuItem(InsertSourceAction.stringId)
        self._application.actionController.removeToolbarButton(InsertSourceAction.stringId)

        try:
            # Это событие появилось только в версии 1.8.0.717
            from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
            pageview = self._getPageView()

            if pageview is not None:
                pageview.Unbind(EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)
        except ImportError:
            pass

    def destroy(self):
        from .actions import InsertSourceAction

        if self._application.mainWindow is not None:
            self._application.actionController.removeAction(InsertSourceAction.stringId)

    def _onTabChanged(self, event):
        self._enableTools()
        event.Skip()

    def _enableTools(self):
        from .actions import InsertSourceAction
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX and
                   not self._application.selectedPage.readonly)
        self._application.actionController.enableTools(InsertSourceAction.stringId, enabled)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView


class OldGuiCreator(BaseGuiCreator):
    """
    Создание элементов интерфейса без использования actions
    """
    def __init__(self, controller, application):
        super(OldGuiCreator, self).__init__(controller, application)
        self.SOURCE_TOOL_ID = u"PLUGIN_SOURCE_TOOL_ID"

    def createTools(self):
        pageView = self._getPageView()

        helpString = _(u"Source Code(:source ...:)")
        image = getImagePath("source.png")

        pageView.addTool(pageView.commandsMenu,
                         self.SOURCE_TOOL_ID,
                         self.__onInsertCommand,
                         helpString,
                         helpString,
                         image)

    def removeTools(self):
        self._getPageView().removeTool(self.SOURCE_TOOL_ID)

    def destroy(self):
        pass

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

    def __onInsertCommand(self, event):
        self._controller.insertCommand()

# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню
"""
from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED

from .i18n import get_
from .actions import LightboxAction


class GUIController(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, application):
        self._application = application

        # Сюда добавить все Actions
        self._actions = [LightboxAction]

        global _
        _ = get_()

    def initialize(self):
        self._application.onPageViewCreate += self._onPageViewCreate
        self._application.onPageViewDestroy += self._onPageViewDestroy

        if self._application.mainWindow is not None:
            self._registerActions()
            if self._isWikiPage(self._application.selectedPage):
                self._onPageViewCreate(self._application.selectedPage)

    def _registerActions(self):
        actionController = self._application.actionController
        [*map(lambda action: actionController.register(
            action(self._application), None), self._actions)]

    def _removeActions(self):
        actionController = self._application.actionController
        [*map(lambda action: actionController.removeAction(action.stringId),
              self._actions)]

    def _createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        # Меню, куда будут добавляться команды
        menu = self._getPageView().commandsMenu

        [*map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)]

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def _removeTools(self):
        if self._application.mainWindow is not None:
            actionController = self._application.actionController
            [*map(lambda action: actionController.removeMenuItem(action.stringId),
                  self._actions)]

            self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)

    def destroy(self):
        self._application.onPageViewCreate -= self._onPageViewCreate
        self._application.onPageViewDestroy -= self._onPageViewDestroy

        if self._application.mainWindow is not None:
            if self._isWikiPage(self._application.selectedPage):
                self._removeTools()

            self._removeActions()

    def _onTabChanged(self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)

        actionController = self._application.actionController
        [*map(lambda action: actionController.enableTools(action.stringId, enabled),
              self._actions)]

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

    def _onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if self._isWikiPage(page):
            self._createTools()

    def _isWikiPage(self, page):
        return page is not None and page.getTypeString() == u"wiki"

    def _onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if self._isWikiPage(page):
            self._removeTools()

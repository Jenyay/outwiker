# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню
"""

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED


class ActionGUIInfo(object):
    def __init__(self, action, menu_id=None,
                 toolbar_id=None, image_fname=None):
        self.action = action
        self.menu_id = menu_id
        self.toolbar_id = toolbar_id
        self.image_fname = image_fname


class ActionsGUIController(object):
    """
    Base class to create GUI for actions
    """
    def __init__(self, application, pageTypeString):
        self._application = application
        self._pageTypeString = pageTypeString
        self._actionsInfoList = []

    def initialize(self, action_gui_info_list):
        self._actionsInfoList = action_gui_info_list[:]

        self._application.onPageViewCreate += self._onPageViewCreate
        self._application.onPageViewDestroy += self._onPageViewDestroy

        self._registerActions()
        if self._isRequestedPageType:
            self._onPageViewCreate(self._application.selectedPage)

    def _registerActions(self):
        actionController = self._application.actionController
        [*map(lambda action_info: actionController.register(
            action_info.action(self._application), None), self._actionsInfoList)]

    def _removeActions(self):
        actionController = self._application.actionController
        [*map(lambda action_info: actionController.removeAction(action_info.action.stringId),
              self._actionsInfoList)]

    def _createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        for action_info in self._actionsInfoList:
            if action_info.menu_id is not None:
                self._application.actionController.appendMenuItem(
                    action_info.action.stringId,
                    mainWindow.menuController[action_info.menu_id])

            if action_info.toolbar_id is not None:
                self._application.actionController.appendToolbarButton(
                    action_info.action.stringId,
                    mainWindow.toolbars[action_info.toolbar_id],
                    action_info.image_fname)

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def _removeTools(self):
        actionController = self._application.actionController

        for action_info in self._actionsInfoList:
            if action_info.menu_id is not None:
                actionController.removeMenuItem(action_info.action.stringId)

            if action_info.toolbar_id is not None:
                actionController.removeToolbarButton(action_info.action.stringId)

        self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED,
                                   handler=self._onTabChanged)

    def destroy(self):
        self._application.onPageViewCreate -= self._onPageViewCreate
        self._application.onPageViewDestroy -= self._onPageViewDestroy

        if self._isRequestedPageType:
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
        [*map(lambda action: actionController.enableTools(action.action.stringId, enabled),
              self._actionsInfoList)]

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

    def _onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if self._isRequestedPageType:
            self._createTools()

    @property
    def _isRequestedPageType(self):
        page = self._application.selectedPage
        return (page is not None and
                page.getTypeString() == self._pageTypeString)

    def _onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if self._isRequestedPageType:
            self._removeTools()

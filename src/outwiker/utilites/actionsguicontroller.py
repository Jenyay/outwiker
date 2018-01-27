# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню
"""

import os.path

from outwiker.core.defines import PAGE_MODE_TEXT


class ActionGUIInfo(object):
    def __init__(self, action, menu_id=None, button_info=None):
        self.action = action
        self.menu_id = menu_id
        self.button_info = button_info


class ButtonInfo(object):
    def __init__(self, toolbar_id, image_fname):
        self.toolbar_id = toolbar_id
        self.image_fname = image_fname


class ActionsGUIController(object):
    """
    Class to create buttons at toolbar and menu items for actions
    """
    def __init__(self, application, pageTypeString):
        self._application = application
        self._pageTypeString = pageTypeString
        self._actionsInfoList = []
        self._new_toolbars = []
        self._new_menus = []

    def initialize(self, action_gui_info_list,
                   new_toolbars=None, new_menus=None):
        '''
        new_toolbars - list of the tuples (toolbar_id, toolbar_title)
        new_menus - list of the tuples (menu_id, title, parent_menu_id)
        '''
        self._actionsInfoList = action_gui_info_list[:]
        self._new_toolbars = new_toolbars[:] if new_toolbars is not None else []
        self._new_menus = new_menus[:] if new_menus is not None else []

        self._application.onPageViewCreate += self._onPageViewCreate
        self._application.onPageViewDestroy += self._onPageViewDestroy

        self._registerActions()
        if self._isRequestedPageType(self._application.selectedPage):
            self._onPageViewCreate(self._application.selectedPage)

    def _registerActions(self):
        actionController = self._application.actionController
        for action_info in self._actionsInfoList:
            actionController.register(action_info.action, None)

    def _removeActions(self):
        actionController = self._application.actionController
        for action_info in self._actionsInfoList:
            actionController.removeAction(action_info.action.stringId)

    def _createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        self._createToolBars()
        self._createMenus()

        for action_info in self._actionsInfoList:
            if action_info.menu_id is not None:
                self._application.actionController.appendMenuItem(
                    action_info.action.stringId,
                    mainWindow.menuController[action_info.menu_id])

            if action_info.button_info is not None:
                assert os.path.exists(action_info.button_info.image_fname)
                self._application.actionController.appendToolbarButton(
                    action_info.action.stringId,
                    mainWindow.toolbars[action_info.button_info.toolbar_id],
                    action_info.button_info.image_fname)

        self._enableTools()

    def _createToolBars(self):
        mainWindow = self._application.mainWindow
        for toolbar_info in self._new_toolbars:
            mainWindow.toolbars.createToolBar(toolbar_info[0], toolbar_info[1])

    def _createMenus(self):
        mainWindow = self._application.mainWindow
        for menu_info in self._new_menus:
            mainWindow.menuController.createSubMenu(menu_id=menu_info[0],
                                                    title=menu_info[1],
                                                    parent_id=menu_info[2])

    def _destroyToolBars(self):
        mainWindow = self._application.mainWindow
        for toolbar_info in self._new_toolbars:
            mainWindow.toolbars.destroyToolBar(toolbar_info[0])

    def _destroyMenus(self):
        mainWindow = self._application.mainWindow
        for menu_info in self._new_menus:
            mainWindow.menuController.removeMenu(menu_info[0])

    def _removeTools(self):
        if self._application.mainWindow is None:
            return

        actionController = self._application.actionController

        for action_info in self._actionsInfoList:
            if action_info.menu_id is not None:
                actionController.removeMenuItem(action_info.action.stringId)

            if action_info.button_info is not None:
                actionController.removeToolbarButton(action_info.action.stringId)

        self._destroyToolBars()
        self._destroyMenus()

    def destroy(self):
        self._application.onPageViewCreate -= self._onPageViewCreate
        self._application.onPageViewDestroy -= self._onPageViewDestroy

        if self._isRequestedPageType(self._application.selectedPage):
            self._removeTools()

        self._removeActions()

    def _onTabChanged(self, page, params):
        self._enableTools()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.GetPageMode() == PAGE_MODE_TEXT and
                   not self._application.selectedPage.readonly)

        actionController = self._application.actionController
        for action_info in self._actionsInfoList:
            actionController.enableTools(action_info.action.stringId, enabled)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pageView

    def _onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if self._isRequestedPageType(page):
            self._createTools()
            self._application.onPageModeChange += self._onTabChanged

    def _isRequestedPageType(self, page):
        return (page is not None and
                page.getTypeString() == self._pageTypeString)

    def _onPageViewDestroy(self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if self._isRequestedPageType(page):
            self._removeTools()
            self._application.onPageModeChange -= self._onTabChanged

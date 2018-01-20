# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
import os.path

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from outwiker.gui.defines import TOOLBAR_PLUGINS

from .i18n import get_

# Импортировать все Actions
from .actions import PluginAction


class GuiCreator(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._application = application

        # Сюда добавить все Actions
        self._actions = [PluginAction]

        # MenuItem создаваемого подменю
        self._submenuItem = None

        global _
        _ = get_()

    def initialize(self):
        if self._application.mainWindow is not None:
            list(map(lambda action: self._application.actionController.register(
                action(self._application), None), self._actions))

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        # Меню, куда будут добавляться команды
        menu = self._getPageView().commandsMenu

        list(map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions))

        # При необходимости добавить кнопки на панель
        toolbar = mainWindow.toolbars[TOOLBAR_PLUGINS]

        self._application.actionController.appendToolbarButton(
            PluginAction.stringId,
            toolbar,
            self._getImagePath("image.png"))

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def _getImagePath(self, imageName):
        """
        Получить полный путь до картинки
        """
        imagedir = os.path.join(os.path.dirname(__file__), "images")
        fname = os.path.join(imagedir, imageName)
        return fname

    def removeTools(self):
        if self._application.mainWindow is not None:
            actionController = self._application.actionController
            list(map(lambda action: actionController.removeMenuItem(action.stringId),
                     self._actions))

            list(map(lambda action: actionController.removeToolbarButton(action.stringId),
                     self._actions))

            self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED,
                                       handler=self._onTabChanged)

    def destroy(self):
        if self._application.mainWindow is not None:
            actionController = self._application.actionController
            list(map(lambda action: actionController.removeAction(action.stringId),
                     self._actions))

    def _onTabChanged(self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)

        actionController = self._application.actionController
        list(map(lambda action: actionController.enableTools(action.stringId, enabled),
                 self._actions))

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

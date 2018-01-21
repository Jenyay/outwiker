# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
import os.path

import wx

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED

from .i18n import get_

# Импортировать все Actions
from .actions import PlotAction, OpenHelpAction


class GuiCreator(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # Сюда добавить все Actions
        self._actions = [PlotAction, OpenHelpAction]

        # Actions, которые должны быть задизаблены в режиме только для чтения
        # и просмотра
        self._disabledActions = [PlotAction]

        # MenuItem создаваемого подменю
        self._submenuItem = None

        self.__toolbarCreated = False
        self.ID_TOOLBAR = u'Plugin_DataGraph'

        global _
        _ = get_()

    def initialize(self):
        if self._application.mainWindow is not None:
            actionController = self._application.actionController
            for action in self._actions:
                actionController.register(action(self._application), None)

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        self._createToolBar()

        # Меню, куда будут добавляться команды
        menu = wx.Menu()

        [*map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)]

        self._submenuItem = self._getPageView().toolsMenu.AppendSubMenu(
            menu,
            _(u"DataGraph")
        )

        # При необходимости добавить кнопки на панель
        toolbar = mainWindow.toolbars[self.ID_TOOLBAR]

        self._application.actionController.appendToolbarButton(
            PlotAction.stringId,
            toolbar,
            self._getImagePath("plot.png"))

        self._application.actionController.appendToolbarButton(
            OpenHelpAction.stringId,
            toolbar,
            self._getImagePath("help.png"))

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def _createToolBar(self):
        """
        Создание панели с кнопками, если она еще не была создана
        """
        if not self.__toolbarCreated:
            mainWnd = self._application.mainWindow
            mainWnd.toolbars.createToolBar(self.ID_TOOLBAR, _('DataGraph'))
            self.__toolbarCreated = True

    def _destroyToolBar(self):
        """
        Уничтожение панели с кнопками
        """
        if self.__toolbarCreated:
            self._application.mainWindow.toolbars.destroyToolBar(self.ID_TOOLBAR)
            self.__toolbarCreated = False

    def _getImagePath(self, imageName):
        """
        Получить полный путь до картинки
        """
        imagedir = os.path.join(os.path.dirname(__file__), "images")
        fname = os.path.join(imagedir, imageName)
        return fname

    def removeTools(self):
        if self._application.mainWindow is not None:
            self._application.mainWindow.toolbars.updatePanesInfo()
            [*map(lambda action: self._application.actionController.removeMenuItem(action.stringId),
                  self._actions)]

            [*map(lambda action: self._application.actionController.removeToolbarButton(action.stringId),
                  self._actions)]

            self._destroyToolBar()

            self._getPageView().toolsMenu.DestroyItem(self._submenuItem)
            self._submenuItem = None

            self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)

    def destroy(self):
        if self._application.mainWindow is not None:
            actionController = self._application.actionController
            for action in self._actions:
                actionController.removeAction(action.stringId)

    def _onTabChanged(self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX and
                   not self._application.selectedPage.readonly)

        [*map(lambda action: self._application.actionController.enableTools(action.stringId, enabled), self._disabledActions)]

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

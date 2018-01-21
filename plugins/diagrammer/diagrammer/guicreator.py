# -*- coding: utf-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
import os.path

import wx

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED

from .i18n import get_

# Импортировать все Actions
from .actions.insertdiagram import InsertDiagramAction
from .actions.help import HelpAction
from .actions.insertnode import InsertNodeAction
from .actions.insertgroup import InsertGroupAction
from .actions.insertedge import (InsertEdgeNoneAction,
                                 InsertEdgeRightAction,
                                 InsertEdgeLeftAction,
                                 InsertEdgeBothAction)


class GuiCreator(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # Сюда добавить все Actions
        self._actions = [InsertDiagramAction,
                         InsertNodeAction,
                         InsertGroupAction,
                         InsertEdgeNoneAction,
                         InsertEdgeLeftAction,
                         InsertEdgeRightAction,
                         InsertEdgeBothAction,
                         HelpAction]

        # MenuItem создаваемого подменю
        self._submenuItem = None

        self.__toolbarCreated = False
        self.ID_TOOLBAR = u"Diagrammer"

        global _
        _ = get_()

    def initialize(self):
        if self._application.mainWindow is not None:
            [*map(lambda action: self._application.actionController.register(
                action(self._application), None), self._actions)]

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        self.__createToolBar()

        # Меню, куда будут добавляться команды
        # menu = self._getPageView().commandsMenu
        menu = wx.Menu()
        self._submenuItem = self.__getParentMenu().AppendSubMenu(
            menu,
            _(u"Diagrammer")
        )

        [*map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)]

        # При необходимости добавить кнопки на панель
        toolbar = mainWindow.toolbars[self.ID_TOOLBAR]

        self._application.actionController.appendToolbarButton(
            InsertDiagramAction.stringId,
            toolbar,
            self._getImagePath("diagram.png"))

        self._application.actionController.appendToolbarButton(
            InsertNodeAction.stringId,
            toolbar,
            self._getImagePath("node.png"))

        self._application.actionController.appendToolbarButton(
            InsertGroupAction.stringId,
            toolbar,
            self._getImagePath("group.png"))

        self._application.actionController.appendToolbarButton(
            InsertEdgeNoneAction.stringId,
            toolbar,
            self._getImagePath("edge-none.png"))

        self._application.actionController.appendToolbarButton(
            InsertEdgeLeftAction.stringId,
            toolbar,
            self._getImagePath("edge-left.png"))

        self._application.actionController.appendToolbarButton(
            InsertEdgeRightAction.stringId,
            toolbar,
            self._getImagePath("edge-right.png"))

        self._application.actionController.appendToolbarButton(
            InsertEdgeBothAction.stringId,
            toolbar,
            self._getImagePath("edge-both.png"))

        self._application.actionController.appendToolbarButton(
            HelpAction.stringId,
            toolbar,
            self._getImagePath("help.png"))

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def __getParentMenu(self):
        return self._getPageView().toolsMenu

    def __createToolBar(self):
        """
        Создание панели с кнопками, если она еще не была создана
        """
        if not self.__toolbarCreated:
            mainWnd = self._application.mainWindow
            mainWnd.toolbars.createToolBar(
                self.ID_TOOLBAR,
                _(u'Diagrammer')
            )

            self.__toolbarCreated = True

    def __destroyToolBar(self):
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
            assert self._getPageView() is not None

            [*map(lambda action: self._application.actionController.removeMenuItem(action.stringId),
                  self._actions)]

            [*map(lambda action: self._application.actionController.removeToolbarButton(action.stringId),
                  self._actions)]

            self.__destroyToolBar()

            self.__getParentMenu().DestroyItem(self._submenuItem)
            self._submenuItem = None

            self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED,
                                       handler=self._onTabChanged)

    def destroy(self):
        if self._application.mainWindow is not None:
            [*map(lambda action: self._application.actionController.removeAction(action.stringId),
                  self._actions)]

    def _onTabChanged(self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX and
                   not self._application.selectedPage.readonly)

        [*map(lambda action: self._application.actionController.enableTools(action.stringId, enabled),
              self._actions)]

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

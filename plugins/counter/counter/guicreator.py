#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
from .misc import getImagePath
from .i18n import get_

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from .actions import InsertCounterAction


class GuiCreator (object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__ (self, controller, application):
        self._controller = controller
        self._application = application


    def initialize (self):
        if self._application.mainWindow != None:
            self._application.actionController.register (
                    InsertCounterAction (self._application, self._controller), 
                    None)


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow == None:
            return

        toolbar = mainWindow.toolbars[mainWindow.PLUGINS_TOOLBAR_STR]

        pageView = self._getPageView()

        self._application.actionController.appendMenuItem (
                InsertCounterAction.stringId, 
                pageView.commandsMenu)

        self._application.actionController.appendToolbarButton (
                InsertCounterAction.stringId,
                toolbar,
                getImagePath ("counter.png"))

        pageView.Bind (EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()


    def removeTools (self):
        self._application.actionController.removeMenuItem (InsertCounterAction.stringId)
        self._application.actionController.removeToolbarButton (InsertCounterAction.stringId)


    def destroy (self):
        if self._application.mainWindow != None:
            self._application.actionController.removeAction (InsertCounterAction.stringId)
            self._getPageView().Unbind (EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)


    def _onTabChanged (self, event):
        self._enableTools()
        
        # Разрешить распространение события дальше
        event.Skip()


    def _enableTools (self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)
        self._application.actionController.enableTools (InsertCounterAction.stringId, enabled)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

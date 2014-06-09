#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from .actions import TitleAction


class GuiCreator (object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__ (self, controller, application):
        self._controller = controller
        self._application = application


    def initialize (self):
        if self._application.mainWindow is not None:
            self._application.actionController.register (
                TitleAction (self._application, self._controller),
                None)


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        pageView = self._getPageView()

        self._application.actionController.appendMenuItem (
            TitleAction.stringId,
            pageView.commandsMenu)

        pageView.Bind (EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()


    def removeTools (self):
        self._application.actionController.removeMenuItem (TitleAction.stringId)


    def destroy (self):
        if self._application.mainWindow is not None:
            self._application.actionController.removeAction (TitleAction.stringId)
            self._getPageView().Unbind (EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)


    def _onTabChanged (self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()


    def _enableTools (self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)
        self._application.actionController.enableTools (TitleAction.stringId, enabled)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

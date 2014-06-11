#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
import wx

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from .actions import TitleAction, DescriptionAction, KeywordsAction, CustomHeadsAction


class GuiCreator (object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__ (self, controller, application):
        self._controller = controller
        self._application = application

        self._actions = [TitleAction,
                         DescriptionAction,
                         KeywordsAction,
                         CustomHeadsAction]
        self._headsMenu = wx.Menu ()

        # MenuItem создаваемого подменю
        self._submenuItem = None


    def initialize (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.register (
                action (self._application, self._controller), None), self._actions)


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        self._submenuItem = self._getParentMenu().AppendSubMenu (self._headsMenu, _(u"HTML Headers"))

        map (lambda action: self._application.actionController.appendMenuItem (
            action.stringId, self._headsMenu), self._actions)

        self._getPageView().Bind (EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()


    def removeTools (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.removeMenuItem (action.stringId),
                 self._actions)

            self._getParentMenu().RemoveItem (self._submenuItem)


    def destroy (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.removeAction (action.stringId),
                 self._actions)

            self._getPageView().Unbind (EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)


    def _onTabChanged (self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()


    def _enableTools (self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)
        self._application.actionController.enableTools (TitleAction.stringId, enabled)


    def _getParentMenu (self):
        return self._getPageView().toolsMenu


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

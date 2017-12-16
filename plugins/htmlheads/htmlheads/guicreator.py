# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
import wx

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from .actions import TitleAction, DescriptionAction, KeywordsAction, CustomHeadsAction
from .i18n import get_


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

        # MenuItem создаваемого подменю
        self._submenuItem = None

        global _
        _ = get_()


    def initialize (self):
        if self._application.mainWindow is not None:
            list(map (lambda action: self._application.actionController.register (
                action (self._application, self._controller), None), self._actions))


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        headsMenu = wx.Menu()

        list(map (lambda action: self._application.actionController.appendMenuItem (
            action.stringId, headsMenu), self._actions))

        self._submenuItem = self._getParentMenu().AppendSubMenu (headsMenu, _(u"HTML Headers"))

        self._getPageView().Bind (EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()


    def removeTools (self):
        if self._application.mainWindow is not None:
            list(map (lambda action: self._application.actionController.removeMenuItem (action.stringId),
                 self._actions))

            self._getParentMenu().DestroyItem (self._submenuItem)
            self._submenuItem = None

            self._getPageView().Unbind (EVT_PAGE_TAB_CHANGED, handler=self._onTabChanged)


    def destroy (self):
        if self._application.mainWindow is not None:
            list(map (lambda action: self._application.actionController.removeAction (action.stringId),
                 self._actions))


    def _onTabChanged (self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()


    def _enableTools (self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)

        list(map (lambda action: self._application.actionController.enableTools (action.stringId, enabled),
             self._actions))


    def _getParentMenu (self):
        return self._getPageView().toolsMenu


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

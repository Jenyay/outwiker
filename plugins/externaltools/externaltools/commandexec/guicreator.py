# -*- coding: UTF-8 -*-

import wx

from outwiker.pages.html.basehtmlpanel import EVT_PAGE_TAB_CHANGED
from externaltools.i18n import get_
from externaltools.commandexec.actions import (
    CommandExecAction,
    MacrosPageAction,
    MacrosHtmlAction,
    MacrosAttachAction,
    MacrosFolderAction,
)


class GuiCreator(object):
    """
    Class for creation user's interface by actions
    """
    def __init__(self, application):
        self._application = application

        self._actions = [
            CommandExecAction,
            MacrosPageAction,
            MacrosHtmlAction,
            MacrosAttachAction,
            MacrosFolderAction,
        ]

        # MenuItem for ExternalTools submenu
        self._submenuItem = None

        global _
        _ = get_()

    def initialize(self):
        if self._application.mainWindow is not None:
            map(lambda action: self._application.actionController.register(
                action(self._application), None),
                self._actions)

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        pluginMenu = wx.Menu()

        map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, pluginMenu), self._actions)

        self._submenuItem = self._getParentMenu().AppendSubMenu(pluginMenu, _(u"ExternalTools"))

        self._getPageView().Bind(EVT_PAGE_TAB_CHANGED, self._onTabChanged)
        self._enableTools()

    def removeTools(self):
        if self._application.mainWindow is not None:
            map(lambda action: self._application.actionController.removeMenuItem(action.stringId),
                self._actions)

            self._getParentMenu().DestroyItem(self._submenuItem)
            self._submenuItem = None

            self._getPageView().Unbind(EVT_PAGE_TAB_CHANGED,
                                       handler=self._onTabChanged)

    def destroy(self):
        if self._application.mainWindow is not None:
            map(lambda action: self._application.actionController.removeAction(action.stringId),
                self._actions)

    def _onTabChanged(self, event):
        self._enableTools()

        # Разрешить распространение события дальше
        event.Skip()

    def _enableTools(self):
        pageView = self._getPageView()
        enabled = (pageView.selectedPageIndex == pageView.CODE_PAGE_INDEX)

        map(lambda action: self._application.actionController.enableTools(action.stringId, enabled),
            self._actions)

    def _getParentMenu(self):
        return self._getPageView().toolsMenu

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView

# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""

import wx

from .i18n import get_
from .sessionstorage import SessionStorage
from .sessioncontroller import SessionController

# Импортировать все Actions
from .saveaction import SaveSessionAction
from .removeaction import RemoveSessionAction


class GuiCreator (object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__ (self, controller, application):
        self._controller = controller
        self._application = application

        # Сюда добавить все Actions
        self._actions = [SaveSessionAction, RemoveSessionAction]

        # Номер позиции в меню, куда будем добавлять свои пункты
        self._menuIndex = 3

        # MenuItem создаваемого подменю
        self._menuItem = None

        # Идентификаторы меню, отвечающие за восстановление сессий
        self._sessionsMenuId = []

        self._menu = wx.Menu()

        global _
        _ = get_()


    def initialize (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.register (
                action (self._application, self), None), self._actions)

        self.createTools()


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        map (lambda action: self._application.actionController.appendMenuItem (
            action.stringId, self._menu), self._actions)

        self._menu.AppendSeparator()
        self.updateMenu()

        self._menuItem = self._getParentMenu().InsertMenu (self._menuIndex, -1, _(u"Sessions"), submenu=self._menu)


    def removeTools (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.removeMenuItem (action.stringId),
                 self._actions)

            self._getParentMenu().RemoveItem (self._menuItem)


    def _getParentMenu (self):
        """
        Возвращает меню, куда будут добавляться действия
        """
        assert self._application.mainWindow is not None

        return self._application.mainWindow.mainMenu.fileMenu


    def destroy (self):
        self.removeTools()

        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.removeAction (action.stringId),
                 self._actions)


    def updateMenu (self):
        """
        В меню обновить список сессий
        """
        self._clearSessionMenu()
        self._addSessionsMenuItems()


    def _addSessionsMenuItems (self):
        sessions = SessionStorage (self._application.config).getSessions()
        for sessionName in sorted (sessions.keys(), key=unicode.lower):
            menuId = wx.NewId()
            self._menu.Append (menuId, sessionName)
            self._application.mainWindow.Bind (wx.EVT_MENU,
                                               self._getSessionRestore (sessions[sessionName]),
                                               id=menuId)
            self._sessionsMenuId.append (menuId)


    def _getSessionRestore (self, session):
        """
        Метод, вовзращающий функцию, вызываемую при выборе пункта меню. За счет замыкания выбирается нужная сессия session.
        """
        return lambda event: SessionController (self._application).restore (session)


    def _clearSessionMenu (self):
        """
        Удалить все пункты меню, связанные с сессиями
        """
        for menuId in self._sessionsMenuId:
            self._menu.Remove (menuId)
            self._application.mainWindow.Unbind (wx.EVT_MENU, id=menuId)

        self._sessionsMenuId = []

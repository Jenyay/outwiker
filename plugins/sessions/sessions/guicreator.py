# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""

import wx

from .i18n import get_

# Импортировать все Actions
from .actions import SaveSessionAction, RemoveSessionAction


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

        self._menu = wx.Menu()

        global _
        _ = get_()


    def initialize (self):
        if self._application.mainWindow is not None:
            map (lambda action: self._application.actionController.register (
                action (self._application), None), self._actions)

        self.createTools()


    def createTools (self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        map (lambda action: self._application.actionController.appendMenuItem (
            action.stringId, self._menu), self._actions)

        self._menu.AppendSeparator()
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

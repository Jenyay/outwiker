# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""

import wx

from hackpage.i18n import get_
from hackpage.actions.changeuid import ChangeUIDAction


class GuiCreator(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # Сюда добавить все Actions
        self._actions = [ChangeUIDAction]

        global _
        _ = get_()

        self._menuItem = None

    def initialize(self):
        if self._application.mainWindow is not None:
            map(lambda action: self._application.actionController.register(
                action(self._application, self._controller), None),
                self._actions)

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        # Меню, куда будут добавляться команды
        menu = wx.Menu()
        self._menuItem = mainWindow.mainMenu.toolsMenu.AppendSubMenu(
            menu,
            u'HackPage')

        map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)

    def destroy(self):
        actionController = self._application.actionController
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            map(lambda action: actionController.removeAction(action.stringId),
                self._actions)
            mainWindow.mainMenu.toolsMenu.RemoveItem(self._menuItem)
            self._menuItem = None

# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель
"""
from .i18n import get_

from hackpage.actions import ChangePageUIDAction


class GuiCreator(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # Сюда добавить все Actions
        self._actions = [ChangePageUIDAction]

        global _
        _ = get_()

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
        menu = mainWindow.mainMenu.toolsMenu

        map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)

    def removeTools(self):
        actionController = self._application.actionController
        if self._application.mainWindow is not None:
            map(lambda action: actionController.removeMenuItem(action.stringId),
                self._actions)

    def destroy(self):
        actionController = self._application.actionController
        if self._application.mainWindow is not None:
            map(lambda action: actionController.removeAction(action.stringId),
                self._actions)

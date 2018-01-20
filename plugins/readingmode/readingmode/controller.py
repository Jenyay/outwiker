# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.defines import MENU_VIEW
from outwiker.gui.defines import TOOLBAR_PLUGINS

from .i18n import get_

# Импортируем action
from .actions import ReadingModeAction


class Controller (object):
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    def initialize(self):
        """
        Создать элементы интерфейса, привязанные к ReadingModeAction.
        """
        # Регистрируем ReadingModeAction
        self._application.actionController.register(
            ReadingModeAction(self._application),
            None)

        mainWindow = self._application.mainWindow
        # Проверяем, что главное окно и панель инструментов созданы
        if (mainWindow is not None and
                TOOLBAR_PLUGINS in mainWindow.toolbars):

            viewMenu = self._application.mainWindow.menuController[MENU_VIEW]
            # Добавляем пункт меню с флажком в меню "Вид"
            self._application.actionController.appendMenuCheckItem(
                ReadingModeAction.stringId,
                viewMenu)

            image = self.getImagePath("book-open.png")
            # Добавляем кнопку-переключатель на панель инструментов
            self._application.actionController.appendToolbarCheckButton(
                ReadingModeAction.stringId,
                mainWindow.toolbars[TOOLBAR_PLUGINS],
                image)

    def getImagePath(self, imageName):
        """
        Получить полный путь до картинки.
        """
        imagedir = os.path.join(os.path.dirname(__file__), "images")
        fname = os.path.join(imagedir, imageName)
        return fname

    def destroy(self):
        """
        Уничтожить (выгрузить) плагин.
        Здесь плагин должен отписаться от всех событий.
        """
        mainWindow = self._application.mainWindow
        # Проверяем, что главное окно и панель инструментов созданы
        if (mainWindow is not None and
                TOOLBAR_PLUGINS in mainWindow.toolbars):

            # Удаляем добавленный пункт меню
            self._application.actionController.removeMenuItem(
                ReadingModeAction.stringId)

            # Удаляем добавленную кнопку
            self._application.actionController.removeToolbarButton(
                ReadingModeAction.stringId)

        # Удаляем зарегистрированный action
        self._application.actionController.removeAction(
            ReadingModeAction.stringId)

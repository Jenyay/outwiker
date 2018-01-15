# -*- coding: UTF-8 -*-

"""
Модули с классами для создания GUI (пунктов меню): для старой версии API и с использованием actions
"""

import wx

from outwiker.gui.defines import MENU_HELP

from .i18n import get_


class OldGuiCreator (object):
    def __init__ (self, controller, application):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

        self.UPDATE_ID = wx.NewId()
        self.SILENCE_UPDATE_ID = wx.NewId()


    def initialize (self):
        if self._application.mainWindow is not None:
            self._createMenu()


    def destroy (self):
        if self._application.mainWindow is not None:
            self._destroyMenu()


    def _destroyMenu (self):
        self._application.mainWindow.Unbind (wx.EVT_MENU, id=self.UPDATE_ID, handler=self.__onCheckUpdate)
        self._helpMenu.Delete (self.UPDATE_ID)

        if self._controller.debug:
            self._helpMenu.Delete (self.SILENCE_UPDATE_ID)


    def _createMenu (self):
        """Добавление пункта меню для проверки обновлений"""
        assert self._application.mainWindow is not None

        self._helpMenu.Append (id=self.UPDATE_ID, text=_(u"Check for Updates..."))
        self._application.mainWindow.Bind (wx.EVT_MENU, self.__onCheckUpdate, id=self.UPDATE_ID)

        if self._controller.debug:
            self._helpMenu.Append (id=self.SILENCE_UPDATE_ID, text=_(u"Silence check for Updates..."))
            self._application.mainWindow.Bind (wx.EVT_MENU, self.__onSilenceCheckUpdate, id=self.SILENCE_UPDATE_ID)


    @property
    def _helpMenu (self):
        return self._application.mainWindow.mainMenu.helpMenu


    def __onCheckUpdate (self, event):
        self._controller.checkForUpdates()


    def __onSilenceCheckUpdate (self, event):
        self._controller.checkForUpdatesSilence()



class ActionGuiCreator (object):
    """
    Создатель интерфейса на основе actions
    """
    def __init__ (self, controller, application):
        self._application = application
        self._controller = controller


    def initialize (self):
        from .actions import CheckForUpdatesAction, CheckForUpdatesSilenceAction

        if self._application.mainWindow is not None:
            self._application.actionController.register (
                CheckForUpdatesAction (self._application, self._controller))

            self._application.actionController.appendMenuItem (
                CheckForUpdatesAction.stringId,
                self._helpMenu)


        if (self._controller.debug and
                self._application.mainWindow is not None):
            self._application.actionController.register (
                CheckForUpdatesSilenceAction (self._application, self._controller))

            self._application.actionController.appendMenuItem (
                CheckForUpdatesSilenceAction.stringId,
                self._helpMenu)


    def destroy (self):
        from .actions import CheckForUpdatesAction, CheckForUpdatesSilenceAction

        if self._application.mainWindow is not None:
            self._application.actionController.removeMenuItem (CheckForUpdatesAction.stringId)
            self._application.actionController.removeAction (CheckForUpdatesAction.stringId)

        # Убрать меню проверки обновлений в молчаливом режиме
        if (self._controller.debug and
                self._application.mainWindow is not None):
            self._application.actionController.removeMenuItem (CheckForUpdatesSilenceAction.stringId)
            self._application.actionController.removeAction (CheckForUpdatesSilenceAction.stringId)


    @property
    def _helpMenu (self):
        return self._application.mainWindow.menuController[MENU_HELP]

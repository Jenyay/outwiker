#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Модуль с классами для добавления пунктов меню и кнопок на панель в зависимости от версии программы (есть поддержка actions или еще нет)
"""
from abc import ABCMeta, abstractmethod

from .misc import getImagePath
from .i18n import get_


class BaseGuiCreator (object):
    __metaclass__ = ABCMeta

    def __init__ (self, controller, application):
        self._controller = controller
        self._application = application


    def initialize (self):
        global _
        _ = get_()


    @abstractmethod
    def createTools (self):
        pass


    @abstractmethod
    def removeTools (self):
        pass

   
    @abstractmethod
    def destroy (self):
        pass



class ActionGuiCreator (BaseGuiCreator):
    """
    Создание элементов интерфейса с использованием actions
    """
    def initialize (self):
        super (ActionGuiCreator, self).initialize()
        from .actions import InsertSourceAction

        self._application.actionController.register (
                InsertSourceAction (self._application, self._controller), 
                None)


    def createTools (self):
        from .actions import InsertSourceAction

        mainWindow = self._application.mainWindow
        toolbar = mainWindow.toolbars[mainWindow.PLUGINS_TOOLBAR_STR]

        pageView = self._getPageView()
        image = getImagePath ("source.png")

        self._application.actionController.appendMenuItem (
                InsertSourceAction.stringId, 
                pageView.commandsMenu)

        self._application.actionController.appendToolbarButton (
                InsertSourceAction.stringId,
                toolbar,
                image)


    def removeTools (self):
        from .actions import InsertSourceAction

        self._application.actionController.removeMenuItem (InsertSourceAction.stringId)
        self._application.actionController.removeToolbarButton (InsertSourceAction.stringId)


    def destroy (self):
        from .actions import InsertSourceAction
        self._application.actionController.removeAction (InsertSourceAction.stringId)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
        


class OldGuiCreator (BaseGuiCreator):
    """
    Создание элементов интерфейса без использования actions
    """
    def __init__ (self, controller, application):
        super (OldGuiCreator, self).__init__ (controller, application)
        self.SOURCE_TOOL_ID = u"PLUGIN_SOURCE_TOOL_ID"


    def createTools (self):
        pageView = self._getPageView()

        helpString = _(u"Source Code (:source ...:)")
        image = getImagePath ("source.png")

        pageView.addTool (pageView.commandsMenu, 
                self.SOURCE_TOOL_ID, 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                image)


    def removeTools (self):
        self._getPageView().removeTool (self.SOURCE_TOOL_ID)


    def destroy (self):
        pass


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
        

    def __onInsertCommand (self, event):
        self._controller.insertCommand()

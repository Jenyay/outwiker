# -*- coding: UTF-8 -*-

import wx

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction


class MainPanesController (object):
    def __init__ (self, application, mainWindow):
        self.__application = application
        self.__mainWindow = mainWindow
        self.auiManager = mainWindow.auiManager

        self.__actions = [ShowHideTreeAction,
                          ShowHideTagsAction,
                          ShowHideAttachesAction]

        self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)

        self.auiManager.SetDockSizeConstraint (0.8, 0.8)


    def createViewMenuItems (self):
        map (lambda action: self.__application.actionController.appendMenuCheckItem (
            action.stringId,
            self.__mainWindow.mainMenu.viewMenu), self.__actions)


    def __onPaneClose (self, event):
        paneName = event.GetPane().name

        for action in self.__getAllActions():
            if paneName == self.auiManager.GetPane (action.getPanel().panel).name:
                self.__application.actionController.check (action.stringId, False)

        event.Skip()


    def __getAllActions (self):
        """
        Возвращает список всех _экземпляров_ действий
        """
        return [self.__application.actionController.getAction (actionType.stringId)
                for actionType in self.__actions]


    def showPanes (self):
        """
        Показать все панели
        """
        map (lambda action: action.getPanel().show(), self.__getAllActions())
        self.auiManager.Update()


    def hidePanes (self):
        """
        Скрыть все панели
        """
        map (lambda action: action.getPanel().hide(), self.__getAllActions())
        self.auiManager.Update()


    def closePanes (self):
        """
        Закрыть все панели
        """
        map (lambda action: action.getPanel().close(), self.__getAllActions())


    def loadPanesSize (self):
        """
        Загрузить размеры всех панелей
        """
        map (lambda action: action.getPanel().loadPaneSize(), self.__getAllActions())
        self.auiManager.Update()


    def savePanesParams (self):
        """
        Сохранить размеры всех панелей
        """
        map (lambda action: action.getPanel().saveParams(), self.__getAllActions())


    def updateViewMenu (self):
        """
        Установить флажки напротив нужных пунктов меню "Вид", относящихся к панелям
        """
        self.__application.actionController.check (ShowHideAttachesAction.stringId,
                                                   self.__mainWindow.attachPanel.isShown())

        self.__application.actionController.check (ShowHideTreeAction.stringId,
                                                   self.__mainWindow.treePanel.isShown())

        self.__application.actionController.check (ShowHideTagsAction.stringId,
                                                   self.__mainWindow.tagsCloudPanel.isShown())

        self.auiManager.Update()

# -*- coding: UTF-8 -*-

import wx

from outwiker.actions.showhideattaches import ShowHideAttachesAction
from outwiker.actions.showhidetree import ShowHideTreeAction
from outwiker.actions.showhidetags import ShowHideTagsAction


class MainPanesController(object):
    def __init__(self, application, mainWindow):
        self.__application = application
        self.__mainWindow = mainWindow
        self.auiManager = mainWindow.auiManager

        self.__actions = [ShowHideTreeAction,
                          ShowHideTagsAction,
                          ShowHideAttachesAction]

        self.auiManager.SetDockSizeConstraint(0.8, 0.8)
        self.auiManager.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)
        self._fullscreenHidden = []

    def createViewMenuItems(self):
        actionController = self.__application.actionController
        list(map(lambda action: actionController.appendMenuCheckItem(
            action.stringId,
            self.__mainWindow.mainMenu.viewMenu), self.__actions))

    def __onPaneClose(self, event):
        paneName = event.GetPane().name
        actionController = self.__application.actionController

        for action in self.__getAllActions():
            panel = action.getPanel().panel
            if paneName == self.auiManager.GetPane(panel).name:
                actionController.check(action.stringId, False)

        event.Skip()

    def __getAllActions(self):
        """
        Возвращает список всех _экземпляров_ действий
        """
        actionController = self.__application.actionController
        return [actionController.getAction(actionType.stringId)
                for actionType in self.__actions]

    def fromFullscreen(self):
        """
        Показать все панели
        """
        for action in self.__getAllActions():
            panel = action.getPanel()
            if panel in self._fullscreenHidden:
                panel.show()

        self.loadPanesSize()
        self.updateViewMenu()
        self._fullscreenHidden = []

    def toFullscreen(self):
        """
        Скрыть все панели
        """
        self._fullscreenHidden = []
        for action in self.__getAllActions():
            panel = action.getPanel()
            if panel.isShown():
                panel.hide()
                self._fullscreenHidden.append(panel)

        self.updateViewMenu()

    def closePanes(self):
        """
        Закрыть все панели
        """
        list(map(lambda action: action.getPanel().close(), self.__getAllActions()))

    def loadPanesSize(self):
        """
        Загрузить размеры всех панелей
        """
        list(map(lambda action: action.getPanel().loadPaneSize(),
            self.__getAllActions()))
        self.auiManager.Update()

    def savePanesParams(self):
        """
        Сохранить размеры всех панелей
        """
        list(map(lambda action: action.getPanel().saveParams(),
            self.__getAllActions()))

    def updateViewMenu(self):
        """
        Установить флажки напротив нужных пунктов меню "Вид",
        относящихся к панелям
        """
        self.__application.actionController.check(
            ShowHideAttachesAction.stringId,
            self.__mainWindow.attachPanel.isShown()
        )

        self.__application.actionController.check(
            ShowHideTreeAction.stringId,
            self.__mainWindow.treePanel.isShown()
        )

        self.__application.actionController.check(
            ShowHideTagsAction.stringId,
            self.__mainWindow.tagsCloudPanel.isShown()
        )

        self.auiManager.Update()

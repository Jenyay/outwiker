# -*- coding: utf-8 -*-

import wx

from outwiker.app.actions.showhideattaches import ShowHideAttachesAction
from outwiker.app.actions.showhidetree import ShowHideTreeAction
from outwiker.app.actions.showhidetags import ShowHideTagsAction

from outwiker.gui.defines import MENU_VIEW


class MainPanesController:
    def __init__(self, application, mainWindow):
        self.__application = application
        self.__mainWindow = mainWindow
        self.auiManager = mainWindow.auiManager

        self.__actions = [ShowHideTreeAction,
                          ShowHideTagsAction,
                          ShowHideAttachesAction]

        self._panels = [
                        # self.__application.mainWindow.treePanel,
                        # self.__application.mainWindow.tagsCloudPanel,
                        # self.__application.mainWindow.attachPanel,
                        ]

        if self.__mainWindow.treePanel is not None:
            self._panels.append(self.__mainWindow.treePanel)

        if self.__mainWindow.tagsCloudPanel is not None:
            self._panels.append(self.__mainWindow.tagsCloudPanel)

        if self.__mainWindow.attachPanel is not None:
            self._panels.append(self.__mainWindow.attachPanel)

        self.auiManager.SetDockSizeConstraint(0.8, 0.8)
        self.auiManager.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)
        self._fullscreenHidden = []

    def createViewMenuItems(self):
        actionController = self.__application.actionController
        viewMenu = self.__application.mainWindow.menuController[MENU_VIEW]
        for action in self.__actions:
            actionController.appendMenuCheckItem(action.stringId, viewMenu)

    def __onPaneClose(self, event):
        paneName = event.GetPane().name
        actionController = self.__application.actionController

        for action, panel in zip(self.__getAllActions(), self._panels):
            if paneName == self.auiManager.GetPane(panel.panel).name:
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
        for panel in self._panels:
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
        for panel in self._panels:
            if panel.isShown():
                panel.hide()
                self._fullscreenHidden.append(panel)

        self.updateViewMenu()

    def closePanes(self):
        """
        Закрыть все панели
        """
        for panel in self._panels:
            panel.close()

    def loadPanesSize(self):
        """
        Загрузить размеры всех панелей
        """
        for panel in self._panels:
            panel.loadPaneSize()

        self.auiManager.Update()

    def savePanesParams(self):
        """
        Сохранить размеры всех панелей
        """
        for panel in self._panels:
            panel.saveParams()

    def updateViewMenu(self):
        """
        Установить флажки напротив нужных пунктов меню "Вид",
        относящихся к панелям
        """
        if self.__mainWindow.attachPanel is not None:
            self.__application.actionController.check(
                ShowHideAttachesAction.stringId,
                self.__mainWindow.attachPanel.isShown()
            )


        if self.__mainWindow.treePanel is not None:
            self.__application.actionController.check(
                ShowHideTreeAction.stringId,
                self.__mainWindow.treePanel.isShown()
            )

        if self.__mainWindow.tagsCloudPanel is not None:
            self.__application.actionController.check(
                ShowHideTagsAction.stringId,
                self.__mainWindow.tagsCloudPanel.isShown()
            )

        self.auiManager.Update()

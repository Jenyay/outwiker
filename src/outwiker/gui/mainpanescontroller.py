#!/usr/bin/python
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

        self.__panes = [self.__mainWindow.attachPanel,
                self.__mainWindow.treePanel,
                self.__mainWindow.tagsCloudPanel]

        self.__actions = [ShowHideTreeAction, 
                ShowHideTagsAction,
                ShowHideAttachesAction]

        self.loadPanesSize()

        self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)

        self.auiManager.SetDockSizeConstraint (0.8, 0.8)
        self.auiManager.Update()


    def createViewMenuItems (self):
        map (lambda action: self.__application.actionController.appendMenuCheckItem (action.stringId, 
                self.__mainWindow.mainMenu.viewMenu), self.__actions)


    def __onPaneClose (self, event):
        paneName = event.GetPane().name

        if paneName == self.auiManager.GetPane (self.__mainWindow.attachPanel.panel).name:
            self.__application.actionController.check (ShowHideAttachesAction.stringId, False)

        elif paneName == self.auiManager.GetPane (self.__mainWindow.treePanel.panel).name:
            self.__application.actionController.check (ShowHideTreeAction.stringId, False)

        elif paneName == self.auiManager.GetPane (self.__mainWindow.tagsCloudPanel.panel).name:
            self.__application.actionController.check (ShowHideTagsAction.stringId, False)

        # for action in self.__actions:
        #     if paneName == self.auiManager.GetPane (action.getPanel().panel).name:
        #         self.__application.actionController.check (action.stringId, False)

        event.Skip()


    def showPanes (self):
        map (lambda pane: pane.show(), self.__panes)
        self.auiManager.Update()


    def hidePanes (self):
        map (lambda pane: pane.hide(), self.__panes)
        self.auiManager.Update()


    def closePanes (self):
        map (lambda pane: pane.close(), self.__panes)


    def loadPanesSize (self):
        map (lambda pane: pane.loadPaneSize(), self.__panes)


    def savePanesParams (self):
        """
        Сохранить размеры панелей
        """
        map (lambda pane: pane.saveParams(), self.__panes)


    def updateViewMenu (self):
        self.__mainWindow.mainMenu.viewFullscreen.Check (self.__mainWindow.IsFullScreen())

        self.__application.actionController.check (ShowHideAttachesAction.stringId, 
                self.__mainWindow.attachPanel.isShown())

        self.__application.actionController.check (ShowHideTreeAction.stringId, 
                self.__mainWindow.treePanel.isShown())

        self.__application.actionController.check (ShowHideTagsAction.stringId, 
                self.__mainWindow.treePanel.isShown())

        self.auiManager.Update()

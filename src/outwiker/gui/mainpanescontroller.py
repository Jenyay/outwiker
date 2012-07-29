#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx


class MainPanesController (object):
    def __init__ (self, mainWnd, auiManager):
        self.__mainWnd = mainWnd
        self.auiManager = auiManager

        self.__panes = [self.__mainWnd.attachPanel,
                self.__mainWnd.treePanel,
                self.__mainWnd.tagsCloudPanel]

        self.loadPanesSize()

        self.auiManager.SetDockSizeConstraint (0.8, 0.8)
        self.auiManager.Update()

        self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)

        self.__mainWnd.Bind(wx.EVT_MENU, self.__onViewTree, self.__mainWnd.mainMenu.viewNotes)
        self.__mainWnd.Bind(wx.EVT_MENU, self.__onViewAttaches, self.__mainWnd.mainMenu.viewAttaches)
        self.__mainWnd.Bind(wx.EVT_MENU, self.__onViewTagsCloud, self.__mainWnd.mainMenu.viewTagsCloud)


    def __onViewTree(self, event):
        self.__showHidePane (self.__mainWnd.treePanel)


    def __onViewTagsCloud (self, event):
        self.__showHidePane (self.__mainWnd.tagsCloudPanel)


    def __onViewAttaches(self, event):
        self.__showHidePane (self.__mainWnd.attachPanel)


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
        map (lambda pane: pane.menuItem.Check (pane.isShown()), self.__panes)
        self.__mainWnd.mainMenu.viewFullscreen.Check (self.__mainWnd.IsFullScreen())


    def __showHidePane (self, panel):
        """
        Показать / скрыть pane с некоторым контролом
        """
        self.savePanesParams()

        if panel.pane.IsShown():
            panel.pane.Hide()
        else:
            panel.pane.Show()

        self.loadPanesSize ()
        self.auiManager.Update()
        self.updateViewMenu()


    def __onPaneClose (self, event):
        for pane in self.__panes:
            if event.GetPane().name == self.auiManager.GetPane (pane.panel).name:
                pane.menuItem.Check (False)

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from exportmenu import ExportMenuFactory


class Controller (object):
    """
    Класс контроллера для интерфейса плагина
    """
    def __init__ (self, owner, application):
        self.__application = application
        self.__owner = owner

        self.__exportMenu = None

        self.EXPORT_SINGLE = wx.NewId()
        self.EXPORT_BRANCH = wx.NewId()


    def __addExportItems (self, menu):
        self.__exportSingleItem = menu.Append (id=self.EXPORT_SINGLE,
                text=_(u"Export Page To HTML..."))

        self.__exportBranchItem = menu.Append (id=self.EXPORT_BRANCH,
                text=_(u"Export Branch To HTML..."))

        self.__application.mainWindow.Bind (wx.EVT_MENU, self.__onSingleExport, id=self.EXPORT_SINGLE)
        self.__application.mainWindow.Bind (wx.EVT_MENU, self.__onBranchExport, id=self.EXPORT_BRANCH)


    def __onSingleExport (self, event):
        print "__onSingleExport"


    def __onBranchExport (self, event):
        print "__onBranchExport"


    def __createMenu (self):
        """
        Создать меню, если есть главное окно
        """
        assert self.__application.mainWindow != None

        factory = ExportMenuFactory (self.__application.mainWindow.mainMenu)
        self.__exportMenu = factory.getExportMenu()

        if self.__exportMenu != None:
            self.__addExportItems (self.__exportMenu)


    def initialize (self):
        if self.__application.mainWindow != None:
            self.__createMenu()


    def destroy (self):
        if self.__exportMenu == None:
            return

        self.__application.mainWindow.Unbind (wx.EVT_MENU, id=self.EXPORT_SINGLE, handler=self.__onSingleExport)
        self.__application.mainWindow.Unbind (wx.EVT_MENU, id=self.EXPORT_BRANCH, handler=self.__onBranchExport)

        self.__exportMenu.DeleteItem (self.__exportSingleItem)
        self.__exportSingleItem = None

        self.__exportMenu.DeleteItem (self.__exportBranchItem)
        self.__exportBranchItem = None

        if (self.__exportMenu.GetMenuItemCount() == 0):
            factory = ExportMenuFactory (self.__application.mainWindow.mainMenu)
            factory.deleteExportMenu()
            self.__exportMenu = None

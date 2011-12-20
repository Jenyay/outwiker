#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx


class Controller (object):
    """
    Класс контроллера для интерфейса плагина
    """
    def __init__ (self, application):
        self.__application = application

        # Номер пункта "Экспорт", если его создаем
        self.__exportMenuPosition = 5

        # Порядковый номер подменю главного меню, куда добавляется пункт "Экспорт"
        self.__fileMenuIndex = 0

        self.__exportMenu = None

        self.EXPORT_SINGLE = wx.NewId()
        self.EXPORT_BRANCH = wx.NewId()
        self.EXPORT_ID = wx.NewId()


    def __getFileMenu (self):
        return self.__application.mainWindow.mainMenu.GetMenu(self.__fileMenuIndex)


    def __getExportMenu (self):
        """
        Найти меню "Экспорт". Если не найдено, создать
        """
        filemenu = self.__getFileMenu()
        if filemenu == None:
            print _(u"Export2Html: File menu not found")
            return

        exportId = filemenu.FindItem (_(u"Export") )
        return filemenu.FindItemById (exportId).GetSubMenu() if exportId != -1 else self.__createExportMenu(filemenu)


    def __createExportMenu (self, menu):
        """
        Создать пункт для подменю "Экспорт"
        menu - меню, в котором должно быть создано подменю
        """
        exportmenu = wx.Menu ()
        menu.InsertMenu (pos=self.__exportMenuPosition, 
                id=self.EXPORT_ID, 
                text=_(u"Export"),
                submenu=exportmenu,
                help=u"")
        return exportmenu


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


    def initialize (self):
        self.__exportMenu = self.__getExportMenu()

        if self.__exportMenu != None:
            self.__addExportItems (self.__exportMenu)


    def destroy (self):
        if self.__exportMenu != None:
            self.__application.mainWindow.Unbind (wx.EVT_MENU, id=self.EXPORT_SINGLE, handler=self.__onSingleExport)
            self.__application.mainWindow.Unbind (wx.EVT_MENU, id=self.EXPORT_BRANCH, handler=self.__onBranchExport)

            self.__exportMenu.DeleteItem (self.__exportSingleItem)
            self.__exportSingleItem = None

            self.__exportMenu.DeleteItem (self.__exportBranchItem)
            self.__exportBranchItem = None

            if self.__exportMenu.GetMenuItemCount() == 0:
                filemenu = self.__getFileMenu()
                assert filemenu != None

                filemenu.Delete (self.EXPORT_ID)
                self.__exportMenu = None



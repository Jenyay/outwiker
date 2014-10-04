# -*- coding: UTF-8 -*-

import wx


class ExportMenuFactory (object):
    """
    Класс для поиска или создания пункта меню "Экспорт"
    """
    def __init__ (self, mainMenuBar):
        self.__mainMenuBar = mainMenuBar

        # Порядковый номер подменю главного меню, куда добавляется пункт "Экспорт"
        self.__fileMenuIndex = 0

        # Номер пункта "Экспорт", если его создаем
        self.__exportMenuPosition = 5

        self.EXPORT_ID = -1

        from .i18n import _
        global _


    def __getFileMenu (self):
        return self.__mainMenuBar.GetMenu(self.__fileMenuIndex)


    def getExportMenu (self):
        """
        Найти меню "Экспорт". Если не найдено, создать
        """
        exportId = self.__findExportId ()

        if exportId != -1:
            return self.__getFileMenu().FindItemById (exportId).GetSubMenu()
        else:
            return self.createExportMenu()


    def deleteExportMenu (self):
        """
        Удалить меню "Экспорт"
        """
        filemenu = self.__getFileMenu()

        if filemenu is None:
            print _(u"File menu not found")
            return

        filemenu.Delete (self.__findExportId())


    def __findExportId (self):
        """
        Получить идентификатор пункта "Экспорт".
        Возвращает -1, если идентификатор не найден
        """
        filemenu = self.__getFileMenu()
        if filemenu is None:
            return -1

        exportId = filemenu.FindItem (_(u"Export"))
        return exportId


    def createExportMenu (self):
        """
        Создать пункт для подменю "Экспорт"
        menu - меню, в котором должно быть создано подменю
        """
        menu = self.__getFileMenu()

        if menu is None:
            print _(u"File menu not found")
            return

        exportmenu = wx.Menu ()
        menu.InsertMenu (pos=self.__exportMenuPosition,
                         id=self.EXPORT_ID,
                         text=_(u"Export"),
                         submenu=exportmenu,
                         help=u"")
        return exportmenu

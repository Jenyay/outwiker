# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.dialogs.messagebox import MessageBox

from .exportmenu import ExportMenuFactory
from .exportpagedialog import ExportPageDialog
from .exportbranchdialog import ExportBranchDialog
from .exceptions import InvalidPageFormat
from .exporterfactory import ExporterFactory


class Controller:
    """
    Класс контроллера для интерфейса плагина
    """

    def __init__(self, owner, application):
        self.__application = application
        self.__owner = owner
        self.__exportMenu = None

    def __addExportItems(self, menu):
        self._exportSingleMenuItem = self.__exportSingleItem = menu.Append(
            id=wx.ID_ANY, item=_("Export Page To HTML...")
        )

        self._exportBranchMenuItem = self.__exportBranchItem = menu.Append(
            id=wx.ID_ANY, item=_("Export Branch To HTML...")
        )

        self.__application.mainWindow.Bind(
            wx.EVT_MENU, self.__onSingleExport, self._exportSingleMenuItem
        )

        self.__application.mainWindow.Bind(
            wx.EVT_MENU, self.__onBranchExport, self._exportBranchMenuItem
        )

    def __onSingleExport(self, event):
        assert self.__application.mainWindow is not None

        if self.__application.selectedPage is None:
            MessageBox(_("Please, select page"), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        try:
            exporter = ExporterFactory.getExporter(self.__application.selectedPage)
        except InvalidPageFormat:
            MessageBox(
                _("This page type not support export to HTML"),
                _("Error"),
                wx.OK | wx.ICON_ERROR,
            )
            return

        dlg = ExportPageDialog(
            self.__application.mainWindow, exporter, self.__application.config
        )

        dlg.ShowModal()
        dlg.Destroy()

    def __onBranchExport(self, event):
        assert self.__application.mainWindow is not None

        if self.__application.wikiroot is None:
            MessageBox(_("Wiki is not open"), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        root = self.__getRootPage()

        dlg = ExportBranchDialog(self.__application, root)
        dlg.ShowModal()
        dlg.Destroy()

    def __getRootPage(self):
        """
        Возвращает страницу, которая будет считаться корнем ветки при экспорте
        """
        if self.__application.selectedPage is None:
            return self.__application.wikiroot

        return self.__application.selectedPage

    def __createMenu(self):
        """
        Создать меню, если есть главное окно
        """
        assert self.__application.mainWindow is not None

        mainMenu = self.__application.mainWindow.menuController.getRootMenu()
        factory = ExportMenuFactory(mainMenu)
        self.__exportMenu = factory.getExportMenu()

        if self.__exportMenu is not None:
            self.__addExportItems(self.__exportMenu)

    def initialize(self):
        from .i18n import _

        global _

        if self.__application.mainWindow is not None:
            self.__createMenu()

    def destroy(self):
        if self.__exportMenu is None:
            return

        self.__application.mainWindow.Unbind(wx.EVT_MENU, handler=self.__onSingleExport)

        self.__application.mainWindow.Unbind(wx.EVT_MENU, handler=self.__onBranchExport)

        self.__exportMenu.Delete(self.__exportSingleItem)
        self.__exportSingleItem = None

        self.__exportMenu.Delete(self.__exportBranchItem)
        self.__exportBranchItem = None

        if self.__exportMenu.GetMenuItemCount() == 0:
            mainMenu = self.__application.mainWindow.menuController.getRootMenu()
            factory = ExportMenuFactory(mainMenu)
            factory.deleteExportMenu()
            self.__exportMenu = None

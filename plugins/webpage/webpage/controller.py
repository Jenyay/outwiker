# -*- coding: UTF-8 -*-

import wx

from outwiker.core.factoryselector import FactorySelector

from webnotepage import WebPageFactory, WebNotePage
from actions.downloadaction import DownloadAction


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application


    def initialize (self):
        self.__menuName = _(u"Web page")
        self._createGui()

        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        FactorySelector.addFactory (WebPageFactory())


    def destroy (self):
        self._removeGui()

        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        FactorySelector.removeFactory (WebPageFactory().getTypeString())


    def _createGui (self):
        if self._application.mainWindow is not None:
            self._createMenu()
            self._createAction()


    def _removeGui (self):
        mainWindow = self._application.mainWindow
        if (mainWindow is not None and
                mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars):
            self._application.actionController.removeMenuItem (DownloadAction.stringId)
            self._application.actionController.removeToolbarButton (DownloadAction.stringId)

            index = mainWindow.mainMenu.FindMenu (self.__menuName)
            assert index != wx.NOT_FOUND

            mainWindow.mainMenu.Remove (index)


    def __onPageDialogPageFactoriesNeeded (self, page, params):
        if (params.pageForEdit is not None and
                params.pageForEdit.getTypeString() == WebNotePage.getTypeString()):
            params.addPageFactory (WebPageFactory())


    def _createMenu (self):
        pass


    def _createAction (self):
        pass

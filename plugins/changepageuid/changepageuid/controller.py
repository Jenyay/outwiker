# -*- coding: UTF-8 -*-

import wx

from outwiker.core.commands import testreadonly
from outwiker.core.exceptions import ReadonlyException

from .i18n import get_
from .guicreator import GuiCreator
from .dialog import ChangeUidDialog
from .dialogcontroller import DialogController


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = None

        self.CHANGE_PAGE_UID = wx.NewId()


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()

        self._application.onTreePopupMenu += self.__onTreePopupMenu

        if self._application.mainWindow is not None:
            self._guiCreator.createTools()


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onTreePopupMenu -= self.__onTreePopupMenu

        self._guiCreator.removeTools()
        self._guiCreator.destroy ()


    def __onTreePopupMenu (self, menu, page):
        menu.Append (self.CHANGE_PAGE_UID, _(u"Change Page Identifier..."))

        self._application.mainWindow.Bind (wx.EVT_MENU,
                                           id=self.CHANGE_PAGE_UID,
                                           handler=self.__onPopupClick)


    def __onPopupClick (self, event):
        self.changeUidWithDialog()
        self._application.mainWindow.Unbind (wx.EVT_MENU,
                                             id=self.CHANGE_PAGE_UID)


    @testreadonly
    def changeUidWithDialog (self):
        """
        Вызвать диалог для изменения UID страницы
        """
        page = self._application.selectedPage

        if page is None:
            return

        if page.readonly:
            raise ReadonlyException

        dlg = ChangeUidDialog (self._application.mainWindow)

        dlgController = DialogController (self._application,
                                          dlg,
                                          self._application.selectedPage)

        resultDlg = dlgController.showDialog ()

        if resultDlg == wx.ID_OK:
            # Не отлавливаем исключения, поскольку считаем,
            # что правильность идентификатора проверил DialogController
            self._application.pageUidDepot.changeUid (page, dlg.uid)

        dlg.Destroy()

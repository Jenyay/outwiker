# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly
import outwiker.core.exceptions

from .i18n import get_
from .sourceconfig import SourceConfig
from .insertdialog import InsertDialog
from .insertdialogcontroller import InsertDialogController


class InsertSourceAction(BaseAction):
    """
    Вызвать диалог для вставки команды (:source:)
    """
    stringId = u"Source_InsertSource"

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Source Code (:source ...:)")

    @property
    def description(self):
        return _(
            u"Source plugin. Insert (: source... :) command for source code highlighting")

    def run(self, params):
        self._insertCommand()

    @testreadonly
    def _insertCommand(self):
        """
        Вставка команды (:source:) в редактор
        """
        if self._application.selectedPage.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        config = SourceConfig(self._application.config)

        with InsertDialog(self._application.mainWindow) as dlg:
            dlgController = InsertDialogController(
                self._application.selectedPage,
                dlg, config)
            resultDlg = dlgController.showDialog()

            if resultDlg == wx.ID_OK:
                command = dlgController.getCommandStrings()
                pageView = self._getPageView()
                pageView.codeEditor.turnText(command[0], command[1])

            dlg.Destroy()

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pageView

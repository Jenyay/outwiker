# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.actions import BaseAction

from ..gui.insertgroupdialog import InsertGroupDialog, InsertGroupController
from ..i18n import get_


class InsertGroupAction(BaseAction):
    """
    Действие для вставки группы объектов
    """
    stringId = "Diagrammer_InsertGroup"

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @property
    def title(self):
        return _("Insert group")

    @property
    def description(self):
        return _("Diagrammer. Insert new group")

    def run(self, params):
        assert self._application.mainWindow is not None

        with InsertGroupDialog(self._application.mainWindow) as dlg:
            controller = InsertGroupController(dlg)
            result = controller.showDialog()

            if result == wx.ID_OK:
                begin, end = controller.getResult()
                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.turnText(begin, end)

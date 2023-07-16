# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.actions import BaseAction

from ..i18n import get_
from ..gui.insertdiagramdialog import (InsertDiagramDialog,
                                       InsertDiagramController)


class InsertDiagramAction(BaseAction):
    """
    Описание действия
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "Diagrammer_InsertDiagram"

    @property
    def title(self):
        return _("Insert diagram")

    @property
    def description(self):
        return _("Diagrammer. Insert diagram")

    def run(self, params):
        assert self._application.mainWindow is not None

        with InsertDiagramDialog(self._application.mainWindow) as dlg:
            controller = InsertDiagramController(dlg)
            result = controller.showDialog()

            if result == wx.ID_OK:
                begin, end = controller.getResult()
                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.turnText(begin, end)

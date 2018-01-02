# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction

from ..gui.insertnodedialog import InsertNodeDialog, InsertNodeController
from ..i18n import get_


class InsertNodeAction(BaseAction):
    """
    Описание действия
    """
    stringId = u"Diagrammer_InsertNode"

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Insert node")

    @property
    def description(self):
        return _(u"Diagrammer. Insert new node")

    def run(self, params):
        assert self._application.mainWindow is not None

        with InsertNodeDialog(self._application.mainWindow) as dlg:
            controller = InsertNodeController(dlg)
            result = controller.showDialog()

            if result == wx.ID_OK:
                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.replaceText(controller.getResult())

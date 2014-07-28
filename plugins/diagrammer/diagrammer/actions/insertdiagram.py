# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from ..i18n import get_


class InsertDiagramAction (BaseAction):
    """
    Описание действия
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Diagrammer_InsertDiagram"


    @property
    def title (self):
        return _(u"Insert diagram")


    @property
    def description (self):
        return _(u"Insert diagram")


    def run (self, params):
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u'(:diagram:)\n', u'\n(:diagramend:)')

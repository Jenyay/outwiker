# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class TexEquationAction (BaseAction):
    """
    Вставка формулы
    """
    stringId = u"WikiEquation"

    def __init__ (self, application):
        self._application = application
        global _
        _ = get_()


    @property
    def title (self):
        return _(u"Equation")


    @property
    def description (self):
        return _(u"Insert the equation in te TeX format")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u'{$', u'$}')

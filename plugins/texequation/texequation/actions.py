# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from texequation.gui.buttonsdialog import ButtonsDialog
from .i18n import get_


class TexEquationAction (BaseAction):
    """
    Insert the equation.
    """
    stringId = u"WikiEquation"

    def __init__(self, application):
        self._application = application
        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Equation")

    @property
    def description(self):
        return _(u"Insert the equation in te TeX format")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        parent = self._application.mainWindow
        message = _(u'Select the equation type')
        caption = _(u'Insert the equation')
        buttons = [_(u'Inline'), _(u'Block'), _(u'Cancel')]
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor

        with ButtonsDialog(parent, message, caption, buttons, cancel=2) as fp:
            result = fp.ShowModal()
            if result == 0:
                codeEditor.turnText(u'{$', u'$}')
            elif result == 1:
                codeEditor.turnText(u'{$$', u'$$}')

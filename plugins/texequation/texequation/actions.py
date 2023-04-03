# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction
from outwiker.api.gui.dialogs import ButtonsDialog

from .i18n import get_


class TexEquationAction(BaseAction):
    """
    Insert the equation.
    """

    stringId = "WikiEquation"

    def __init__(self, application):
        self._application = application
        global _
        _ = get_()

    @property
    def title(self):
        return _("Equation...")

    @property
    def description(self):
        return _("Insert the equation in te TeX format")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        parent = self._application.mainWindow
        message = _("Select the equation type")
        caption = _("Insert the equation")
        buttons = [_("Inline"), _("Block"), _("Cancel")]
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor

        with ButtonsDialog(parent, message, caption, buttons, cancel=2) as fp:
            result = fp.ShowModal()
            if result == 0:
                codeEditor.turnText("{$", "$}")
            elif result == 1:
                codeEditor.turnText("{$$", "$$}")

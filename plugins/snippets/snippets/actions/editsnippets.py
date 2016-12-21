# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from snippets.i18n import get_
from snippets.gui.editdialog import EditSnippetsDialogController


class EditSnippetsAction (BaseAction):
    stringId = u"snippets_edit_snippets"

    def __init__(self, application):
        super(EditSnippetsAction, self).__init__()
        self._application = application
        global _
        _ = get_()
        self._dialogController = EditSnippetsDialogController(application)

    def run(self, params):
        self._dialogController.ShowDialog()

    @property
    def title(self):
        return _(u"Snippets management...")

    @property
    def description(self):
        return _(u'Snippets. Open dialog to edit, create or remove snippets.')

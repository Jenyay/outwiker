# -*- coding: UTF-8 -*-

from collections import namedtuple

from outwiker.core.event import Event
from outwiker.gui.testeddialog import TestedDialog

from snippets.snippetparser import SnippetParser


FinishDialogParams = namedtuple('FinishDialogParams', ['text'])


class VariablesDialog(TestedDialog):
    def setTemplate(self, template):
        pass

    def prepare(self, variables):
        pass


class VariablesDialogController(object):
    def __init__(self, application):
        self._application = application

        self.onFinishDialog = Event()
        self._dialog = None
        self._parser = None
        self._selectedText = u''

    def ShowDialog(self, selectedText, template):
        if self._dialog is None:
            self._dialog = VariablesDialog(self._application.mainWindow)

        self._selectedText = selectedText
        self._parser = SnippetParser(template, self._application)
        variables = sorted([var for var
                            in self._parser.getVariables()
                            if not var.startswith('__')])

        self._dialog.setTemplate(template)
        self._dialog.prepare(variables)

        if variables:
            self._dialog.Show()
        else:
            self._finishDialog()

    def destroy(self):
        self.onFinishDialog.clear()
        if self._dialog is not None:
            self._dialog.Close()
            self._dialog = None

    def _finishDialog(self):
        if self._application.selectedPage is not None:
            text = self._parser.process(self._selectedText,
                                        self._application.selectedPage)
            self.onFinishDialog(FinishDialogParams(text))
        self._dialog.Close()
        self._dialog = None

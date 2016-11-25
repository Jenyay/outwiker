# -*- coding: utf-8 -*-

from outwiker.gui.texteditor import TextEditor


class SnippetEditor(TextEditor):
    def __init__(self, parent, application):
        self._application = application
        super(SnippetEditor, self).__init__(parent)

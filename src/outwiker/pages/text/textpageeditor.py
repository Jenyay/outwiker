# -*- coding: utf-8 -*-

from outwiker.core.application import Application
from outwiker.gui.baseeditordroptarget import BaseEditorDropTarget
from outwiker.gui.texteditor import TextEditor


class TextPageEditor(TextEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.dropTarget = TextEditorDropTarget(Application, self)


class TextEditorDropTarget(BaseEditorDropTarget):
    """
    Class to drag files to the text editor
    """
    def correctAttachFileName(self, fname):
        return fname

    def correctFileName(self, fname):
        return fname

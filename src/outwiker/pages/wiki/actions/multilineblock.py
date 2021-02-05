# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.pages.wiki.parser.tokenmultilineblock import MultilineBlockToken


class MultilineBlockAction(BaseAction):
    """
    Insert the tags for multiline block for wiki notation
    """
    stringId = 'MultilineBlock'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('Multiline block [{…}]')

    @property
    def description(self):
        return _('Insert a multiline block')

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText(MultilineBlockToken.start, MultilineBlockToken.end)

# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.defines import (STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   )

from ..wikistyleutils import (turnBlockOrInline,
                              isSelectedBlock,
                              getCustomStylesNames,
                              )


class WikiStyleOnlyAction (BaseAction):
    """
    MArk text with style name
    """
    stringId = u"WikiStyleOnly"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Text style")

    @property
    def description(self):
        return _(u"Apply style to text")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        styles_folder = (STYLES_BLOCK_FOLDER_NAME if isSelectedBlock(editor)
                         else STYLES_INLINE_FOLDER_NAME)
        styles = getCustomStylesNames(styles_folder)

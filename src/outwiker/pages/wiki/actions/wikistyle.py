# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.defines import (STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   )
from outwiker.core.system import getSpecialDirList

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
        dir_list = getSpecialDirList(styles_folder)
        styles = sorted(getCustomStylesNames(dir_list))

        title = _('Select style')
        message = _('Styles')
        mainWindow = self._application.mainWindow

        with wx.SingleChoiceDialog(mainWindow, message, title, styles) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                style = dlg.GetStringSelection()
                text_begin = '%{style}%'.format(style=style)
                text_end = '%%'
                turnBlockOrInline(editor, text_begin, text_end)

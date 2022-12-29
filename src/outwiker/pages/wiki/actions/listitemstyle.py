# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.pages.wiki.parser.tokenlist import ListToken
import outwiker.pages.wiki.gui.listitemstyledialog as lis


class ListItemStyleAction(BaseAction):
    """
    Show dialog to select list item style (bullet)
    """
    stringId = 'ListItemStyle'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('List item style...')

    @property
    def description(self):
        return _('Select list item style (bullet)')

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None
        assert self._application.selectedPage is not None

        editor = self._application.mainWindow.pagePanel.pageView.codeEditor
        line_number = editor.GetCurrentLine()
        line_str = editor.GetLine(line_number)
        cursor_position = editor.GetCurrentPosition()

        # Find end of list markers
        list_token_end = 0
        while list_token_end < len(line_str):
            substr = line_str[list_token_end:]
            if substr.startswith(ListToken.unorderList):
                list_token_end += len(ListToken.unorderList)
            else:
                break

        prefix = ' '
        suffix = ''
        if list_token_end == 0:
            prefix = ListToken.unorderList + ' '

        with lis.ListItemStyleDialog(self._application.mainWindow) as dlg:
            controller = lis.ListItemStyleDialogController(dlg)
            if controller.ShowModal() == wx.ID_OK:
                style_str = controller.GetStyle()
                if not list_token_end and style_str:
                    suffix = ' '

                if list_token_end and not style_str and not suffix:
                    prefix = ''

                insert_str = '{prefix}{style}{suffix}'.format(prefix=prefix, style=style_str, suffix=suffix)

                new_line_str = line_str[: list_token_end] + insert_str + line_str[list_token_end:]
                new_position = cursor_position + len(insert_str)
                editor.SetLine(line_number, new_line_str)
                editor.SetCurrentPosition(new_position)

# -*- coding: utf-8 -*-

from typing import Tuple
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

        with lis.ListItemStyleDialog(self._application.mainWindow) as dlg:
            controller = lis.ListItemStyleDialogController(dlg)
            if controller.ShowModal() == wx.ID_OK:
                style_str = controller.GetStyle()
                editor = self._application.mainWindow.pagePanel.pageView.codeEditor
                first_line, last_line = editor.GetSelectionLines()
                new_lines_str = []
                for line_number in range(first_line, last_line + 1):
                    new_lines_str.append(self._process_line(editor, line_number, style_str))

                new_text = '\n'.join(new_lines_str)
                first_line_pos, last_line_pos = self._get_selection_full_lines(editor)
                editor.SetSelection(first_line_pos, last_line_pos)
                editor.replaceText(new_text)

    def _get_selection_full_lines(self, editor) -> Tuple[int, int]:
        startSelection = editor.GetSelectionStart()
        endSelection = editor.GetSelectionEnd()

        text = editor.GetText()

        if len(text) == 0:
            return (0, 0)

        firstLinePos = text[:startSelection].rfind("\n")
        lastLinePos = text[endSelection:].find("\n")

        if firstLinePos == -1:
            firstLinePos = 0
        else:
            firstLinePos += 1

        if lastLinePos == -1:
            lastLinePos = len(text)
        else:
            lastLinePos += endSelection

        return (firstLinePos, lastLinePos)

    def _process_line(self, editor, line_number, style_str) -> str:
        line_str = editor.GetLine(line_number)
        if line_str.endswith('\n'):
            line_str = line_str[:-1]

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

        if not list_token_end and style_str:
            suffix = ' '

        if list_token_end and not style_str and not suffix:
            prefix = ''

        insert_str = '{prefix}{style}{suffix}'.format(prefix=prefix, style=style_str, suffix=suffix)

        return line_str[: list_token_end] + insert_str + line_str[list_token_end:]

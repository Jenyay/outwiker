# -*- coding: utf-8 -*-

import re


def listComplete_generic(editor: 'outwiker.gui.texeditor.TextEditor',
                         list_regexp: str,
                         ) -> bool:
    '''
    Process the Enter key pressing to complete lists.
    editor - instance of the TextEditor
    list_regexp - wiki list regular expression

    Returns True if enterPressed() change text else returns False.
    '''
    regexp = re.compile(list_regexp, re.I)
    current_line = editor.GetCurrentLineText()
    current_line_number = editor.GetCurrentLine()
    line_start_position = 0 if current_line_number == 0 else editor.GetLineEndPosition(current_line_number - 1) + 1
    cursor_position = editor.GetSelectionEnd()
    line_cursor_position = cursor_position - line_start_position

    if editor.GetSelectionStart() != cursor_position:
        return False

    match = regexp.search(current_line)
    if match is None:
        return False

    list_text = match.group(0)

    if len(list_text.rstrip()) > line_cursor_position:
        return False

    if current_line == list_text:
        editor.DelLineLeft()
        return True

    editor.replaceText('\n' + list_text)
    return True


def listComplete_wiki(editor: 'outwiker.gui.texeditor.TextEditor') -> bool:
    '''
    Process the Enter key pressing to complete lists.
    editor - instance of the TextEditor

    Returns True if enterPressed() change text else returns False.
    '''
    wiki_regexp = r'^[*#]+\s*'
    return listComplete_generic(editor, wiki_regexp)

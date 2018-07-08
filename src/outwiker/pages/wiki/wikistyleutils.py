# -*- coding: utf-8 -*-

import wx

from outwiker.core.standardcolors import StandardColors


def turnBlockOrInline(editor, text_begin, text_end):
    '''
    Turn text like "text_begin ... text_end" for inline string or
    "text_begin
    ...
    text_end"

    for block string.
    '''
    sel_text = editor.GetSelectedText()

    if isSelectedBlock(editor):
        if not sel_text.startswith('\n'):
            text_begin = text_begin + '\n'
        if not sel_text.endswith('\n'):
            text_end = '\n' + text_end

    editor.turnText(text_begin, text_end)


def isSelectedBlock(editor):
    sel_start = editor.GetSelectionStart()
    sel_end = editor.GetSelectionEnd()
    full_text = editor.GetText()
    text_length = len(full_text)

    # If selected full paragraph (full line)
    is_begin_line = (sel_start == 0) or (full_text[sel_start - 1] == '\n')
    is_end_line = (sel_end == text_length or
                   sel_end == text_length - 1 or
                   full_text[sel_end + 1] == '\n')

    return is_begin_line and is_end_line


def selectColor(parent, title):
    '''
    Select color with dialog
    '''
    color_data = wx.ColourData()
    color_data.SetChooseFull(True)
    with wx.ColourDialog(parent, color_data) as dialog:
        dialog.SetTitle(title)
        if dialog.ShowModal() == wx.ID_OK:
            selected_color_data = dialog.GetColourData()
            color = selected_color_data.GetColour()
            color_str = color.GetAsString(wx.C2S_HTML_SYNTAX).lower()
            if color_str in StandardColors:
                color_str = StandardColors[color_str]

            return color_str

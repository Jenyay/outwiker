# -*- coding: utf-8 -*-

import os
from typing import Dict

import wx

from outwiker.core.config import Config, JSONOption
from outwiker.gui.defines import RECENT_COLORS_COUNT
from outwiker.gui.testeddialog import TestedColourDialog
from outwiker.utilites.textfile import readTextFile


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
    is_end_line = sel_end == text_length or full_text[sel_end] == '\n'

    return is_begin_line and is_end_line


def selectColor(parent, title, colorsList):
    '''
    Select color with dialog
    '''
    color_data = wx.ColourData()
    color_data.SetChooseFull(True)
    for n, color in enumerate(colorsList[:RECENT_COLORS_COUNT]):
        color_data.SetCustomColour(n, color)

    if colorsList:
        color_data.SetColour(colorsList[0])

    with TestedColourDialog(parent, color_data) as dialog:
        dialog.SetTitle(title)
        if dialog.ShowModal() == wx.ID_OK:
            selected_color_data = dialog.GetColourData()
            color = selected_color_data.GetColour()
            color_str = color.GetAsString(wx.C2S_HTML_SYNTAX).lower()

            return color_str


def loadCustomStyles(dir_list):
    styles = {}
    extension = '.css'

    for folder in dir_list:
        for fname in os.listdir(folder):
            if fname.endswith(extension):
                name = fname[:-len(extension)]
                try:
                    css = readTextFile(os.path.join(folder, fname))
                    styles[name] = css
                except IOError:
                    pass
    return styles


def loadCustomStylesFromConfig(config: Config,
                               section_name: str,
                               option_name: str) -> Dict[str, str]:
    '''
    Load saved styles from page config in JSON format.
    Return dictionary: key - style name, value - CSS style.
    '''
    result = {}
    opt = JSONOption(config, section_name, option_name, None)
    styles = opt.value
    if not isinstance(styles, dict):
        return result

    result = {
        name: value
        for name, value in styles.items()
        if isinstance(name, str) and isinstance(value, str)
    }
    return result


def saveCustomStylesToConfig(config: Config,
                             section_name: str,
                             option_name: str,
                             styles: Dict[str, str]) -> None:
    '''
    Save custom styles to config in JSON format
    '''
    opt = JSONOption(config, section_name, option_name, None)
    opt.value = styles


def getCustomStylesNames(dir_list):
    styles = []
    extension = '.css'

    for folder in dir_list:
        styles += [fname[: -len(extension)]
                   for fname
                   in os.listdir(folder)
                   if fname.endswith(extension)]

    return list(set(styles))

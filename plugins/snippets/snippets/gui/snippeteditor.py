# -*- coding: utf-8 -*-

import re

import wx

from outwiker.gui.controls.texteditorbase import TextEditorBase


class SnippetEditor(TextEditorBase):
    def __init__(self, parent):
        super(SnippetEditor, self).__init__(parent)

        self.STYLE_VARIABLE = 1
        self.STYLE_COMMENT = 2
        self.STYLE_STATEMENT = 3

        self.textCtrl.StyleSetSpec(self.STYLE_VARIABLE, "fore:#2255a5")
        self.textCtrl.StyleSetSpec(self.STYLE_COMMENT, "fore:#10a526")
        self.textCtrl.StyleSetSpec(self.STYLE_STATEMENT, "fore:#c409bb")

        self._variable_re = re.compile(r'{{.*?}}', re.U | re.M)
        self._comment_re = re.compile(r'{#.*?#}', re.U | re.M)
        self._statement_re = re.compile(r'{%.*?%}', re.U | re.M)

        self.textCtrl.SetMarginWidth(0, 35)
        self.textCtrl.SetMarginWidth(1, 5)
        self.textCtrl.Bind(wx.stc.EVT_STC_STYLENEEDED, self._onStyleNeeded)
        self._bindStandardMenuItems()

    def _onStyleNeeded(self, event):
        fulltext = self._getTextForParse()
        textlength = self._helper.calcByteLen(fulltext)
        stylelist = [0] * textlength

        self._colorize(stylelist,
                       fulltext,
                       self._variable_re,
                       self.STYLE_VARIABLE)

        self._colorize(stylelist,
                       fulltext,
                       self._statement_re,
                       self.STYLE_STATEMENT)

        self._colorize(stylelist,
                       fulltext,
                       self._comment_re,
                       self.STYLE_COMMENT)

    def _colorize(self, stylelist, fulltext, regexp, style):
        matches = regexp.finditer(fulltext)
        for match in matches:
            start = match.start()
            end = match.end()
            bytepos_start = self._helper.calcBytePos(fulltext, start)
            bytepos_end = self._helper.calcBytePos(fulltext, end)

            self.textCtrl.StartStyling(bytepos_start, 0xff)
            textlength = bytepos_end - bytepos_start
            self.textCtrl.SetStyling(textlength, style)

# -*- coding: utf-8 -*-

import wx

from markdownparser.tokens.tokenfonts import (FontsFactory,
                                              BoldToken,
                                              ItalicToken,
                                              BoldItalicToken)
from markdownparser.tokens.tokentext import TextFactory
from markdownparser.tokens.tokenheading import HeadingFactory
from markdownparser.tokens.tokenlink import LinkFactory

from outwiker.gui.texteditorhelper import TextEditorHelper


class MarkdownColorizer(object):
    def __init__(self, editor, colorizeSyntax, enableSpellChecking, runEvent):
        self._editor = editor
        self._helper = TextEditorHelper()
        self._enableSpellChecking = enableSpellChecking
        self._runEvent = runEvent

        self.text = TextFactory.make()
        self.bold = FontsFactory.makeBold()
        self.italic = FontsFactory.makeItalic()
        self.bold_italic = FontsFactory.makeBoldItalic()
        self.heading = HeadingFactory.make()
        self.link = LinkFactory.make()
        self.code = FontsFactory.makeCode()
        self.comment = FontsFactory.makeComment()

        if colorizeSyntax:
            self.colorParser = (
                self.heading |
                self.text |
                self.link |
                self.bold_italic |
                self.bold |
                self.italic |
                self.code |
                self.comment
            )

            self.insideBlockParser = (
                self.text |
                self.link |
                self.bold_italic |
                self.bold |
                self.italic |
                self.comment
            )
        else:
            self.colorParser = self.text
            self.insideBlockParser = self.text

    def colorize(self, text):
        textlength = self._helper.calcByteLen(text)
        stylelist = [0] * textlength
        spellStatusFlags = [True] * len(text)
        self._colorizeText(text,
                           0,
                           textlength,
                           self.colorParser,
                           stylelist,
                           spellStatusFlags)
        wx.CallAfter(self._editor.markSpellErrors, spellStatusFlags)
        return stylelist

    def _checkSpell(self, text, start, end, spellStatusFlags):
        spellChecker = self._editor.getSpellChecker()
        errors = spellChecker.findErrors(text[start: end])

        for _word, err_start, err_end in errors:
            spellStatusFlags[err_start + start:
                             err_end + start] = [False] * (err_end - err_start)

    def _colorizeText(self, text, start, end, parser,
                      stylelist, spellStatusFlags):
        tokens = parser.scanString(text[start: end])

        for token in tokens:
            if not self._runEvent.is_set():
                break

            pos_start = token[1] + start
            pos_end = token[2] + start

            tokenname = token[0].getName()

            if (tokenname == "text" or
                    tokenname == "noformat" or
                    tokenname == "preformat"):
                if self._enableSpellChecking:
                    self._checkSpell(text, pos_start, pos_end,
                                     spellStatusFlags)
                continue

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self._helper.calcBytePos(text, pos_start)
            bytepos_end = self._helper.calcBytePos(text, pos_end)

            # Применим стиль
            if tokenname == "bold":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_BOLD_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(text,
                                   pos_start + len(BoldToken.start_1),
                                   pos_end - len(BoldToken.end_1),
                                   self.insideBlockParser,
                                   stylelist, spellStatusFlags)

            elif tokenname == "italic":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_ITALIC_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(text,
                                   pos_start + len(ItalicToken.start_1),
                                   pos_end - len(ItalicToken.end_1),
                                   self.insideBlockParser, stylelist,
                                   spellStatusFlags)

            elif tokenname == "bold_italic":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_BOLD_ITALIC_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(text,
                                   pos_start + len(BoldItalicToken.start),
                                   pos_end - len(BoldItalicToken.end),
                                   self.insideBlockParser,
                                   stylelist, spellStatusFlags)

            elif tokenname == "heading":
                self._helper.setStyle(stylelist,
                                      self._editor.STYLE_HEADING_ID,
                                      bytepos_start,
                                      bytepos_end)
                if self._enableSpellChecking:
                    self._checkSpell(text, pos_start, pos_end,
                                     spellStatusFlags)

            elif tokenname == "link":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_LINK_ID,
                                      bytepos_start,
                                      bytepos_end)
                if self._enableSpellChecking:
                    self._linkSpellChecking(text,
                                            stylelist,
                                            spellStatusFlags,
                                            pos_start,
                                            pos_end,
                                            token)

            elif tokenname == "code":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_COMMAND_ID,
                                      bytepos_start,
                                      bytepos_end)

            elif tokenname == "comment":
                self._helper.setStyle(stylelist,
                                      self._editor.STYLE_COMMENT_ID,
                                      bytepos_start,
                                      bytepos_end)
                if self._enableSpellChecking:
                    self._checkSpell(text, pos_start, pos_end,
                                     spellStatusFlags)

    def _linkSpellChecking(self, text, stylelist, spellStatusFlags,
                           pos_start, pos_end, token):
        self._checkSpell(text,
                         pos_start + 1,
                         pos_start + 1 + len(token[0][0]),
                         spellStatusFlags)
        link = token[0][1]
        space_pos = link.find(u' ')
        if space_pos != -1:
            self._checkSpell(text,
                             pos_start + 1 + len(token[0][0]) + 2 + space_pos,
                             pos_start + 1 + len(token[0][0]) + 2 + space_pos +
                             len(token[0][1]),
                             spellStatusFlags)

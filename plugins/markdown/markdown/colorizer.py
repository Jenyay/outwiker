# -*- coding: UTF-8 -*-

from parser.tokenfonts import (FontsFactory,
                               BoldToken,
                               ItalicToken,
                               BoldItalicToken)
from parser.tokentext import TextFactory
from parser.tokenheading import HeadingFactory
from parser.tokenlink import LinkFactory

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
        # self.underline = FontsFactory.makeUnderline(None)
        # self.command = CommandFactory.make (None).setParseAction(lambda s, l, t: None)
        # self.url = UrlFactory.make (None).setParseAction(lambda s, l, t: None)
        # self.linebreak = LineBreakFactory.make (None).setParseAction(lambda s, l, t: None)
        # self.noformat = NoFormatFactory.make (None).setParseAction(lambda s, l, t: None)
        # self.preformat = PreFormatFactory.make (None).setParseAction(lambda s, l, t: None)

        if colorizeSyntax:
            self.colorParser = (
                # self.url |
                self.heading |
                self.text |
                # self.linebreak |
                self.link |
                # self.noformat |
                # self.preformat |
                self.bold_italic |
                self.bold |
                self.italic
                # self.underline |
            )

            self.insideBlockParser = (
                # self.url |
                self.text |
                # self.linebreak |
                self.link |
                # self.noformat |
                # self.preformat |
                self.bold_italic |
                self.bold |
                self.italic
                # self.underline
            )
        else:
            self.colorParser = self.text
            self.insideBlockParser = self.text

    def colorize(self, fullText):
        textlength = self._helper.calcByteLen(fullText)
        stylelist = [0] * textlength
        self._colorizeText(fullText,
                           fullText,
                           0,
                           textlength,
                           self.colorParser,
                           stylelist)

        return stylelist

    def _colorizeText(self, fullText, text, start, end, parser, stylelist):
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
                    self._editor.runSpellChecking(stylelist,
                                                  fullText,
                                                  pos_start,
                                                  pos_end)
                continue

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self._helper.calcBytePos (text, pos_start)
            bytepos_end = self._helper.calcBytePos (text, pos_end)

            # Применим стиль
            if tokenname == "bold":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_BOLD_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(fullText,
                                   text,
                                   pos_start + len (BoldToken.start_1),
                                   pos_end - len (BoldToken.end_1),
                                   self.insideBlockParser, stylelist)

            elif tokenname == "italic":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_ITALIC_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(fullText,
                                   text,
                                   pos_start + len (ItalicToken.start_1),
                                   pos_end - len (ItalicToken.end_1),
                                   self.insideBlockParser, stylelist)

            elif tokenname == "bold_italic":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_BOLD_ITALIC_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(fullText,
                                   text,
                                   pos_start + len (BoldItalicToken.start),
                                   pos_end - len (BoldItalicToken.end),
                                   self.insideBlockParser, stylelist)

            # elif tokenname == "underline":
            #     self._helper.addStyle(stylelist,
            #                           self._editor.STYLE_UNDERLINE_ID,
            #                           bytepos_start,
            #                           bytepos_end)
            #     self._colorizeText(fullText,
            #                        text,
            #                        pos_start + len (UnderlineToken.start),
            #                        pos_end - len (UnderlineToken.end),
            #                        self.insideBlockParser,
            #                        stylelist)
            #
            elif tokenname == "heading":
                self._helper.setStyle(stylelist,
                                      self._editor.STYLE_HEADING_ID,
                                      bytepos_start,
                                      bytepos_end)
                if self._enableSpellChecking:
                    self._editor.runSpellChecking(stylelist,
                                                  fullText,
                                                  pos_start,
                                                  pos_end)

            elif tokenname == "link":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_LINK_ID,
                                      bytepos_start,
                                      bytepos_end)
                if self._enableSpellChecking:
                    self._linkSpellChecking(fullText,
                                            text,
                                            stylelist,
                                            pos_start,
                                            pos_end,
                                            token)

            # elif tokenname == "url":
            #     self._helper.addStyle(stylelist,
            #                           self._editor.STYLE_LINK_ID,
            #                           bytepos_start,
            #                           bytepos_end)

    def _linkSpellChecking (self, fullText, text, stylelist, pos_start, pos_end, token):
        self._editor.runSpellChecking(stylelist,
                                      fullText,
                                      pos_start + 1,
                                      pos_start + 1 + len(token[0][0]))
        link = token[0][1]
        space_pos = link.find(u' ')
        if space_pos != -1:
            self._editor.runSpellChecking(stylelist,
                                          fullText,
                                          pos_start + 1 + len(token[0][0]) + 2 + space_pos,
                                          pos_start + 1 + len(token[0][0]) + 2 + space_pos + len(token[0][1]))

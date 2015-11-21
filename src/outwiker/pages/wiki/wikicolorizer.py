# -*- coding: UTF-8 -*-

from parser.tokenfonts import FontsFactory, BoldToken, ItalicToken, BoldItalicToken, UnderlineToken
from parser.tokenheading import HeadingFactory
from parser.tokencommand import CommandFactory
from parser.tokenlink import LinkFactory
from parser.tokenurl import UrlFactory
from parser.tokenlinebreak import LineBreakFactory
from parser.tokennoformat import NoFormatFactory
from parser.tokenpreformat import PreFormatFactory
from parser.tokentext import TextFactory

from outwiker.gui.texteditorhelper import TextEditorHelper


class WikiColorizer (object):
    def __init__ (self, editor, colorizeSyntax, enableSpellChecking, runEvent):
        self._editor = editor
        self._helper = TextEditorHelper()
        self._enableSpellChecking = enableSpellChecking
        self._runEvent = runEvent

        self.text = TextFactory.make (None)
        self.bold = FontsFactory.makeBold (None).setParseAction(lambda s, l, t: None)
        self.italic = FontsFactory.makeItalic (None).setParseAction(lambda s, l, t: None)
        self.bold_italic = FontsFactory.makeBoldItalic (None).setParseAction(lambda s, l, t: None)
        self.underline = FontsFactory.makeUnderline (None).setParseAction(lambda s, l, t: None)
        self.heading = HeadingFactory.make (None).setParseAction(lambda s, l, t: None)
        self.command = CommandFactory.make (None).setParseAction(lambda s, l, t: None)
        self.link = LinkFactory.make (None).setParseAction(lambda s, l, t: None)
        self.url = UrlFactory.make (None).setParseAction(lambda s, l, t: None)
        self.linebreak = LineBreakFactory.make (None).setParseAction(lambda s, l, t: None)
        self.noformat = NoFormatFactory.make (None).setParseAction(lambda s, l, t: None)
        self.preformat = PreFormatFactory.make (None).setParseAction(lambda s, l, t: None)

        if colorizeSyntax:
            self.colorParser = (
                self.url |
                self.text |
                self.linebreak |
                self.link |
                self.noformat |
                self.preformat |
                self.command |
                self.bold_italic |
                self.bold |
                self.italic |
                self.underline |
                self.heading)

            self.insideBlockParser = (
                self.url |
                self.text |
                self.linebreak |
                self.link |
                self.noformat |
                self.preformat |
                self.bold_italic |
                self.bold |
                self.italic |
                self.underline)
        else:
            self.colorParser = self.text
            self.insideBlockParser = self.text


    def colorize (self, fullText):
        textlength = self._helper.calcByteLen (fullText)
        stylelist = [0] * textlength
        self._colorizeText (fullText, fullText, 0, textlength, self.colorParser, stylelist)

        return stylelist


    def _colorizeText (self, fullText, text, start, end, parser, stylelist):
        tokens = parser.scanString (text[start: end])

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
                    self._editor.runSpellChecking (stylelist,
                                                   fullText,
                                                   pos_start,
                                                   pos_end)
                continue

            if tokenname == "linebreak":
                continue

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self._helper.calcBytePos (text, pos_start)
            bytepos_end = self._helper.calcBytePos (text, pos_end)

            # Применим стиль
            if tokenname == "bold":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_BOLD_ID,
                                       bytepos_start,
                                       bytepos_end)
                self._colorizeText (fullText,
                                    text,
                                    pos_start + len (BoldToken.start),
                                    pos_end - len (BoldToken.end),
                                    self.insideBlockParser, stylelist)

            elif tokenname == "italic":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_ITALIC_ID,
                                       bytepos_start,
                                       bytepos_end)
                self._colorizeText (fullText,
                                    text,
                                    pos_start + len (ItalicToken.start),
                                    pos_end - len (ItalicToken.end),
                                    self.insideBlockParser, stylelist)

            elif tokenname == "bold_italic":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_BOLD_ITALIC_ID,
                                       bytepos_start,
                                       bytepos_end)
                self._colorizeText (fullText,
                                    text,
                                    pos_start + len (BoldItalicToken.start),
                                    pos_end - len (BoldItalicToken.end),
                                    self.insideBlockParser, stylelist)

            elif tokenname == "underline":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_UNDERLINE_ID,
                                       bytepos_start,
                                       bytepos_end)
                self._colorizeText (fullText,
                                    text,
                                    pos_start + len (UnderlineToken.start),
                                    pos_end - len (UnderlineToken.end),
                                    self.insideBlockParser,
                                    stylelist)

            elif tokenname == "heading":
                self._helper.setStyle (stylelist,
                                       self._editor.STYLE_HEADING_ID,
                                       bytepos_start,
                                       bytepos_end)
                if self._enableSpellChecking:
                    self._editor.runSpellChecking (stylelist,
                                                   fullText,
                                                   pos_start,
                                                   pos_end)

            elif tokenname == "command":
                self._helper.setStyle (stylelist,
                                       self._editor.STYLE_COMMAND_ID,
                                       bytepos_start,
                                       bytepos_end)

            elif tokenname == "link":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_LINK_ID,
                                       bytepos_start,
                                       bytepos_end)
                self._linkSpellChecking (fullText,
                                         text,
                                         stylelist,
                                         pos_start,
                                         pos_end)

            elif tokenname == "url":
                self._helper.addStyle (stylelist,
                                       self._editor.STYLE_LINK_ID,
                                       bytepos_start,
                                       bytepos_end)


    def _linkSpellChecking (self, fullText, text, stylelist, pos_start, pos_end):
        separator1 = u'->'
        separator2 = u'|'

        link = text[pos_start: pos_end]
        sep1_pos = link.find (separator1)
        if sep1_pos != -1:
            if self._enableSpellChecking:
                self._editor.runSpellChecking (stylelist,
                                               fullText,
                                               pos_start,
                                               pos_start + sep1_pos)
            return

        sep2_pos = link.find (separator2)
        if sep2_pos != -1:
            if self._enableSpellChecking:
                self._editor.runSpellChecking (stylelist,
                                               fullText,
                                               pos_start + sep2_pos + len (separator2),
                                               pos_end)

# -*- coding: utf-8 -*-

import wx

from .parser.tokenfonts import FontsFactory, BoldToken, ItalicToken, BoldItalicToken, UnderlineToken
from .parser.tokenheading import HeadingFactory
from .parser.tokencommand import CommandFactory
from .parser.tokenlink import LinkFactory
from .parser.tokenurl import UrlFactory
from .parser.tokenlinebreak import LineBreakFactory
from .parser.tokennoformat import NoFormatFactory
from .parser.tokenpreformat import PreFormatFactory
from .parser.tokentext import TextFactory
from .parser.tokencomment import CommentFactory
from .parser.tokenattach import AttachFactory
from .parser.tokenthumbnail import ThumbnailFactory

from outwiker.gui.texteditorhelper import TextEditorHelper
from outwiker.gui.stylinginfo import StylingInfo


class WikiColorizer:
    def __init__(self, editor, colorizeSyntax, enableSpellChecking, runEvent):
        self._editor = editor
        self._helper = TextEditorHelper()
        self._enableSpellChecking = enableSpellChecking
        self._runEvent = runEvent

        self.text = TextFactory.make(None)
        self.bold = FontsFactory.makeBold(
            None).setParseAction(lambda s, l, t: None)
        self.italic = FontsFactory.makeItalic(
            None).setParseAction(lambda s, l, t: None)
        self.bold_italic = FontsFactory.makeBoldItalic(
            None).setParseAction(lambda s, l, t: None)
        self.underline = FontsFactory.makeUnderline(
            None).setParseAction(lambda s, l, t: None)
        self.heading = HeadingFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.command = CommandFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.link = LinkFactory.make(None).setParseAction(lambda s, l, t: None)
        self.url = UrlFactory.make(None).setParseAction(lambda s, l, t: None)
        self.linebreak = LineBreakFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.noformat = NoFormatFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.preformat = PreFormatFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.comment = CommentFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.attachment = AttachFactory.make(
            None).setParseAction(lambda s, l, t: None)
        self.thumbnail = ThumbnailFactory.make(
            None).setParseAction(lambda s, l, t: None)

        if colorizeSyntax:
            self.colorParser = (
                self.url |
                self.thumbnail |
                self.attachment |
                self.text |
                self.linebreak |
                self.link |
                self.noformat |
                self.preformat |
                self.comment |
                self.command |
                self.bold_italic |
                self.bold |
                self.italic |
                self.underline |
                self.heading)

            self.insideBlockParser = (
                self.url |
                self.thumbnail |
                self.attachment |
                self.text |
                self.linebreak |
                self.link |
                self.noformat |
                self.preformat |
                self.comment |
                self.bold_italic |
                self.bold |
                self.italic |
                self.underline)
        else:
            self.colorParser = self.text
            self.insideBlockParser = self.text

    def colorize(self, fullText):
        textlength = self._helper.calcByteLen(fullText)
        stylelist = [0] * textlength
        spellStatusFlags = [True] * len(fullText)
        self._colorizeText(fullText, 0, textlength,
                           self.colorParser, stylelist, spellStatusFlags)
        return StylingInfo(stylelist, spellStatusFlags)

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

            if tokenname == "linebreak":
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
                                   pos_start + len(BoldToken.start),
                                   pos_end - len(BoldToken.end),
                                   self.insideBlockParser,
                                   stylelist, spellStatusFlags)

            elif tokenname == "italic":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_ITALIC_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(text,
                                   pos_start + len(ItalicToken.start),
                                   pos_end - len(ItalicToken.end),
                                   self.insideBlockParser,
                                   stylelist, spellStatusFlags)

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

            elif tokenname == "underline":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_UNDERLINE_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._colorizeText(text,
                                   pos_start + len(UnderlineToken.start),
                                   pos_end - len(UnderlineToken.end),
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

            elif tokenname == "command":
                self._helper.setStyle(stylelist,
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

            elif tokenname == "attach":
                self._helper.setStyle(stylelist,
                                      self._editor.STYLE_ATTACHMENT_ID,
                                      bytepos_start,
                                      bytepos_end)

            elif tokenname == "thumbnail":
                self._helper.setStyle(stylelist,
                                      self._editor.STYLE_THUMBNAIL_ID,
                                      bytepos_start,
                                      bytepos_end)

            elif tokenname == "link":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_LINK_ID,
                                      bytepos_start,
                                      bytepos_end)
                self._linkSpellChecking(text,
                                        pos_start,
                                        pos_end,
                                        stylelist,
                                        spellStatusFlags)

            elif tokenname == "url":
                self._helper.addStyle(stylelist,
                                      self._editor.STYLE_LINK_ID,
                                      bytepos_start,
                                      bytepos_end)

    def _linkSpellChecking(self, text, pos_start, pos_end,
                           stylelist, spellStatusFlags):
        separator1 = u'->'
        separator2 = u'|'

        link = text[pos_start: pos_end]
        sep1_pos = link.find(separator1)
        if sep1_pos != -1:
            if self._enableSpellChecking:
                self._checkSpell(text, pos_start, pos_start + sep1_pos,
                                 spellStatusFlags)
            return

        sep2_pos = link.find(separator2)
        if sep2_pos != -1:
            if self._enableSpellChecking:
                self._checkSpell(text, pos_start + sep2_pos + len(separator2),
                                 pos_end, spellStatusFlags)

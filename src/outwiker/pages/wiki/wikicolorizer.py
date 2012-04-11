#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import wx.stc

import threading

from parser.tokenfonts import FontsFactory
from parser.tokenheading import HeadingFactory
from parser.tokencommand import CommandFactory
from parser.tokenlink import LinkFactory
from parser.tokenurl import UrlFactory

ApplyStyleEvent, EVT_APPLY_STYLE = wx.lib.newevent.NewEvent()


class WikiColorizer (object):
    def __init__ (self, editor):
        self._editor = editor

        self.bold = FontsFactory.makeBold (None).setParseAction(lambda s, l, t: None).setResultsName ("bold")

        self.italic = FontsFactory.makeItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("italic")

        self.bold_italic = FontsFactory.makeBoldItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("bold_italic")

        self.underline = FontsFactory.makeUnderline (None).setParseAction(lambda s, l, t: None).setResultsName ("underline")

        self.heading = HeadingFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("heading")

        self.command = CommandFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("command")

        self.link = LinkFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("link")
        
        self.url = UrlFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("link")

        self.colorParser = (self.command | 
                self.bold_italic | 
                self.bold | 
                self.italic | 
                self.underline | 
                self.heading | 
                self.link | 
                self.url)

        self.insideBlockParser = (self.bold_italic | 
                self.bold | 
                self.italic | 
                self.underline | 
                self.link | 
                self.url)

        self._thread = None


    def start (self, text):
        if (self._thread == None or
                not self._thread.isAlive()):
            self._thread = threading.Thread (None, self._threadFunc, args=(text,))
            self._thread.start()


    def _threadFunc (self, text):
        stylebytes = self._startColorize (text)
        event = ApplyStyleEvent (text=text, stylebytes=stylebytes)
        wx.PostEvent (self._editor, event)


    def _startColorize (self, text):
        textlength = self._editor.calcByteLen (text)
        stylelist = [wx.stc.STC_STYLE_DEFAULT] * textlength

        self._colorizeText (text, 0, textlength, self.colorParser, stylelist)

        stylebytes = "".join ([chr(byte) for byte in stylelist])
        return stylebytes


    def _colorizeText (self, text, start, end, parser, stylelist):
        tokens = parser.scanString (text[start: end])

        for token in tokens:
            pos_start = token[1] + start
            pos_end = token[2] + start

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self._editor.calcBytePos (text, pos_start)
            bytepos_end = self._editor.calcBytePos (text, pos_end)

            # Применим стиль
            if token[0].getName() == "bold":
                self._addStyle (stylelist, self._editor.STYLE_BOLD_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, self.insideBlockParser, stylelist)

            elif token[0].getName() == "italic":
                self._addStyle (stylelist, self._editor.STYLE_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 2, pos_end - 2, self.insideBlockParser, stylelist)

            elif token[0].getName() == "bold_italic":
                self._addStyle (stylelist, self._editor.STYLE_BOLD_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 4, pos_end - 4, self.insideBlockParser, stylelist)

            elif token[0].getName() == "underline":
                self._addStyle (stylelist, self._editor.STYLE_UNDERLINE_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 2, pos_end - 2, self.insideBlockParser, stylelist)

            elif token[0].getName() == "heading":
                self._setStyle (stylelist, self._editor.STYLE_HEADING_ID, bytepos_start, bytepos_end)

            elif token[0].getName() == "command":
                self._setStyle (stylelist, self._editor.STYLE_COMMAND_ID, bytepos_start, bytepos_end)

            elif token[0].getName() == "link":
                self._addStyle (stylelist, self._editor.STYLE_LINK_ID, bytepos_start, bytepos_end)


    def _addStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [styleid if style == wx.stc.STC_STYLE_DEFAULT else style | styleid for style in style_src]
        
        stylelist[bytepos_start: bytepos_end] = style_new


    def _setStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        stylelist[bytepos_start: bytepos_end] = [styleid] * (bytepos_end - bytepos_start)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex

from .tokencommand import CommandFactory


class AlignFactory (object):
    @staticmethod
    def make (parser):
        return AlignToken(parser).getToken()


class AlignToken (object):
    """
    Токен для выравнивания
    """
    def __init__ (self, parser):
        self.parser = parser


    def _alignText (self, s, l, t):
        return u'<div align="' + t["align"].lower() + '">' + self.parser.parseWikiMarkup (t["text"]) + '</div>' + t["end"]


    def _alignCommand (self, s, l, t):
        return u'<div align="' + t["align"].lower() + '">' + t[1] + '</div>'


    def getToken (self):
        start = Regex ("%\\s*(?P<align>(left)|(right)|(center)|(justify))\\s*%",
                re.I | re.U)

        text = Regex ("(?P<text>.*?)(?P<end>(\n\n)|\Z)", re.M | re.S | re.I | re.U)
        command = CommandFactory.make(self.parser)

        alignText = start + text
        alignText.setParseAction(self._alignText)

        alignCommand = start + command
        alignCommand.setParseAction (self._alignCommand)

        align = alignCommand | alignText
        align = align(u"alignment")

        return align

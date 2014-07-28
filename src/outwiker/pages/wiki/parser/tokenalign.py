#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


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

        text = Regex (r'''(?P<text>
        .*?
        (\(:\s*(?P<name>\w+).*?:\)
        (.*?                           # Контент между (:name:) и (:nameend:)
        \(:\s*(?P=name)end\s*:\))?.*?)*?)
        (?P<end>(\n\n)|\Z)''',
                      re.M | re.S | re.I | re.U | re.X)

        alignText = start + text
        alignText.setParseAction(self._alignText)
        alignText = alignText(u"alignment")

        return alignText

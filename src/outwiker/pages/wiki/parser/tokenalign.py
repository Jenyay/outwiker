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
    

    def _align (self, s, l, t):
        return u'<DIV ALIGN="' + t["align"].upper() + '">' + self.parser.parseWikiMarkup (t["text"]) + '</DIV>' + t["end"]


    def getToken (self):
        alignRegex = "%\\s*(?P<align>\\w+)\\s*%(?P<text>.*?)(?P<end>(\n\n)|\Z)"

        return Regex (alignRegex, 
                re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction(self._align)("alignment")

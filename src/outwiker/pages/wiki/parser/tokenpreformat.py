# -*- coding: UTF-8 -*-

import html

from outwiker.libs.pyparsing import QuotedString


class PreFormatFactory (object):
    """
    Фабрика для создания токена "без форматирования"ы
    """
    @staticmethod
    def make (parser):
        return PreFormatToken(parser).getToken()


class PreFormatToken (object):
    preFormatStart = "[@"
    preFormatEnd = "@]"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        return QuotedString(PreFormatToken.preFormatStart,
                            endQuoteChar=PreFormatToken.preFormatEnd,
                            multiline=True,
                            convertWhitespaceEscapes=False).setParseAction(self.__convertPreformat)("preformat")


    def __convertPreformat (self, s, l, t):
        return u"<pre>" + html.escape (t[0], True) + u"</pre>"

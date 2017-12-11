# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString
from .utils import noConvert


class NoFormatFactory (object):
    """
    Фабрика для создания токена "без форматирования"ы
    """
    @staticmethod
    def make (parser):
        return NoFormatToken(parser).getToken()


class NoFormatToken (object):
    noFormatStart = "[="
    noFormatEnd = "=]"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        return QuotedString(NoFormatToken.noFormatStart,
                            endQuoteChar=NoFormatToken.noFormatEnd,
                            multiline=True,
                            convertWhitespaceEscapes=False).setParseAction(noConvert)("noformat")

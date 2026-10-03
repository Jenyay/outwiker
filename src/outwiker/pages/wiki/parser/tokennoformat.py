# -*- coding: utf-8 -*-

from pyparsing import QuotedString

from .utils import noConvert


class NoFormatFactory(object):
    """
    Фабрика для создания токена "без форматирования"
    """

    @staticmethod
    def make(parser):
        return NoFormatToken(parser).getToken()


class NoFormatToken(object):
    noFormatStart = "[="
    noFormatEnd = "=]"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(
            self.noFormatStart,
            end_quote_char=self.noFormatEnd,
            multiline=True,
            convert_whitespace_escapes=False,
        ).set_parse_action(noConvert)("noformat")

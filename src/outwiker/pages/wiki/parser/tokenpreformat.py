# -*- coding: utf-8 -*-

import html

from pyparsing import QuotedString


class PreFormatFactory(object):
    """
    Фабрика для создания токена "без форматирования"ы
    """

    @staticmethod
    def make(parser):
        return PreFormatToken(parser).getToken()


class PreFormatToken(object):
    preFormatStart = "[@"
    preFormatEnd = "@]"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(
            PreFormatToken.preFormatStart,
            end_quote_char=PreFormatToken.preFormatEnd,
            multiline=True,
            convert_whitespace_escapes=False,
        ).set_parse_action(self.__convertPreformat)("preformat")

    def __convertPreformat(self, s, l, t):
        return "<pre>" + html.escape(t[0], False) + "</pre>"

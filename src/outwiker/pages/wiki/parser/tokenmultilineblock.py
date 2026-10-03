# -*- coding: utf-8 -*-

from pyparsing import QuotedString

# from .tokenblock import SimpleNestedBlock
# from .tokenlinebreak import LineBreakToken


class MultilineBlockFactory(object):
    """
    The fabric to create multiline block.
    """

    @staticmethod
    def make(parser):
        return MultilineBlockToken(parser).getToken()


class MultilineBlockToken:
    start = "[{"
    end = "}]"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(
            MultilineBlockToken.start,
            end_quote_char=MultilineBlockToken.end,
            multiline=True,
            convert_whitespace_escapes=False,
        ).set_parse_action(self.__convertMultilineBlock)("block")

    def __convertMultilineBlock(self, s, l, t):
        return self.parser.parseTextLevelMarkup(t[0])

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
        return QuotedString(MultilineBlockToken.start,
                            endQuoteChar=MultilineBlockToken.end,
                            multiline=True,
                            convertWhitespaceEscapes=False).setParseAction(self.__convertMultilineBlock)("block")

    def __convertMultilineBlock(self, s, l, t):
        return self.parser.parseTextLevelMarkup(t[0])

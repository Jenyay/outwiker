#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi

from outwiker.libs.pyparsing import QuotedString
from tokenblock import BlockToken


class QuoteFactory (object):
    """
    Фабрика для создания токена для цитат
    """
    @staticmethod
    def make (parser):
        return QuoteToken(parser).getToken()


class QuoteToken (BlockToken):
    quoteStart = "[>"
    quoteEnd = "<]"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (QuoteToken.quoteStart, 
                endQuoteChar = QuoteToken.quoteEnd, 
                multiline = True).setParseAction(self.convertToHTML("<blockquote>","</blockquote>"))("quote")

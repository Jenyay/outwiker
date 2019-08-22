# -*- coding: utf-8 -*-

from pyparsing import QuotedString


class LinkFactory (object):
    @staticmethod
    def make():
        return LinkToken().getToken()


class LinkToken (object):
    def getToken(self):
        token = (QuotedString('[',
                              endQuoteChar=']',
                              convertWhitespaceEscapes=False)('comment') +
                 QuotedString('(',
                              endQuoteChar=')',
                              convertWhitespaceEscapes=False).leaveWhitespace()('url'))('link')
        return token

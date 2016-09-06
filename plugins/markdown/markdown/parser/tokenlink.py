# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString


class LinkFactory (object):
    @staticmethod
    def make():
        return LinkToken().getToken()


class LinkToken (object):
    def getToken(self):
        token = (QuotedString('[', endQuoteChar=']')('comment') +
                 QuotedString('(', endQuoteChar=')').leaveWhitespace()('url'))('link')
        return token

# -*- coding: utf-8 -*-

from pyparsing import QuotedString


class LinkFactory:
    @staticmethod
    def make():
        return LinkToken().getToken()


class LinkToken:
    def getToken(self):
        token = (
            QuotedString("[", endQuoteChar="]", convertWhitespaceEscapes=False)(
                "comment"
            )
            + QuotedString(
                "(", endQuoteChar=")", convertWhitespaceEscapes=False
            ).leaveWhitespace()("url")
        )("link")
        return token

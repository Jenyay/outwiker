# -*- coding: utf-8 -*-

from pyparsing import QuotedString


class LinkFactory:
    @staticmethod
    def make():
        return LinkToken().getToken()


class LinkToken:
    def getToken(self):
        token = (
            QuotedString("[", end_quote_char="]", convert_whitespace_escapes=False)(
                "comment"
            )
            + QuotedString(
                "(", end_quote_char=")", convert_whitespace_escapes=False
            ).leave_whitespace()("url")
        )("link")
        return token

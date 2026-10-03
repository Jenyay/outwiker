# -*- coding: utf-8 -*-

from pyparsing import QuotedString


class CommentFactory:
    """
    A factory to make a comment token
    """

    @staticmethod
    def make(parser):
        return CommentToken(parser).getToken()


class CommentToken:
    commentStart = "<!--"
    commentEnd = "-->"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(
            self.commentStart,
            end_quote_char=self.commentEnd,
            multiline=True,
            convert_whitespace_escapes=False,
        ).set_parse_action(self.__convertComment)("comment")

    def __convertComment(self, s, l, t):
        return ""

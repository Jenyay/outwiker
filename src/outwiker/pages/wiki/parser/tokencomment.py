# -*- coding: utf-8 -*-

from outwiker.libs.pyparsing import QuotedString


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
            endQuoteChar=self.commentEnd,
            multiline=True,
            convertWhitespaceEscapes=False).setParseAction(self.__convertComment)("comment")

    def __convertComment(self, s, l, t):
        return ''

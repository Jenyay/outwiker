#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Literal, Regex


class LineJoinFactory (object):
    @staticmethod
    def make (parser):
        return LineJoinToken().getToken()


class LineJoinToken (object):
    """
    Токен для горизонтальной линии
    """
    def getToken (self):
        token = Regex (r"\\\r?\n")
        token = token.setParseAction (lambda s, l, t: u"")("linejoin")
        return token

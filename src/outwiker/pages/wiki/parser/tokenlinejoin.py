#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

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
        token = Regex (r"\\r?\n", re.MULTILINE)
        token.setParseAction (lambda s, l, t: u"")
        return token

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, Word, CharsNotIn, OneOrMore


class TextFactory (object):
    @staticmethod
    def make (parser):
        return TextToken().getToken()


class TextToken (object):
    """
    Токен для обычного текста
    """
    def getToken (self):
        textRegex = "[\w]+"
        token = Regex (textRegex, re.MULTILINE | re.DOTALL | re.UNICODE)
        token.leaveWhitespace().suppress()
        return token

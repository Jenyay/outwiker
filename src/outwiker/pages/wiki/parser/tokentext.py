# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class TextFactory (object):
    @staticmethod
    def make (parser):
        return TextToken().getToken()


class TextToken (object):
    '''
    Токен для обычного текста
    '''
    def getToken (self):
        textRegex = r'(?:(?:\w-\w)|\w)+'
        token = Regex (textRegex)('text')
        token.leaveWhitespace()
        return token

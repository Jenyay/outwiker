# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class TextFactory(object):
    @staticmethod
    def make():
        return TextToken().getToken()


class TextToken(object):
    '''
    Token for simple text
    '''
    def getToken(self):
        textRegex = r'(?:(?:[^\W_]-[^\W_])|[^\W_])+'
        token = Regex(textRegex, re.UNICODE)('text')
        token.leaveWhitespace()
        return token

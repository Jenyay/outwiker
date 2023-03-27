# -*- coding: utf-8 -*-

import re

from pyparsing import Regex


class TextFactory:
    @staticmethod
    def make():
        return TextToken().getToken()


class TextToken:
    """
    Token for simple text
    """

    def getToken(self):
        textRegex = r"(?:(?:[^\W_]-[^\W_])|[^\W_])+"
        token = Regex(textRegex, re.UNICODE)("text")
        token.leaveWhitespace()
        return token

# -*- coding: utf-8 -*-

import re

from pyparsing import Regex, LineEnd


class HeadingFactory:
    @staticmethod
    def make():
        return HeadingToken().getToken()


class HeadingToken:
    def __init__(self):
        self._token_1 = Regex(r"^#+\s+(\\\n|.)*$", re.M | re.U)
        self._token_2 = (
            Regex(r".+", re.M | re.U)
            + LineEnd()
            + Regex(r"((-+)|(=+))", re.M | re.U).setWhitespaceChars(" \t")
            + LineEnd()
        )

    def getToken(self):
        return (self._token_1 | self._token_2)("heading")

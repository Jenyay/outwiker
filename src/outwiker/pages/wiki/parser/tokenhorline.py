# -*- coding: utf-8 -*-

from pyparsing import Regex


class HorLineFactory:
    @staticmethod
    def make(parser):
        return HorLineToken().getToken()


class HorLineToken:
    """
    Токен для горизонтальной линии
    """

    def getToken(self):
        return Regex("----+").setParseAction(lambda s, l, t: "<hr>")("horline")

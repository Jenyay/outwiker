#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Regex


class HorLineFactory (object):
    @staticmethod
    def make (parser):
        return HorLineToken().getToken()


class HorLineToken (object):
    """
    Токен для горизонтальной линии
    """
    def getToken (self):
        return Regex("----+").setParseAction (lambda s, l, t: "<hr>")("horline")


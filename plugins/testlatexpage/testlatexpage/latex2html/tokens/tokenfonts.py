# -*- coding: UTF-8 -*-

import re

from ..libs.pyparsing import Regex


class FontsFactory (object):
    """
    Фабрика для создания шрифтовых / блочных токенов
    """
    @staticmethod
    def makeItalic (parser):
        """
        Создать токен для курсивного шрифта
        """
        return ItalicToken(parser).getToken()



class ItalicToken (object):
    """
    Токен для курсива
    """
    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        reg = r"\{\\it\s+(?P<text>.+?)\s*\}"

        return Regex (reg,
                      flags=re.M | re.S | re.I | re.U).setParseAction (
                          self.convertToHTML (u"<i>", u"</i>"))("italic")


    def convertToHTML (self, opening, closing):
        """
        opening - открывающийся тег(и)
        closing - закрывающийся тег(и)
        """
        def conversionParseAction (s, l, t):
            return u"".join ([opening, t["text"], closing])

        return conversionParseAction

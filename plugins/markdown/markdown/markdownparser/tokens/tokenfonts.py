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


    @staticmethod
    def makeBold (parser):
        """
        Создать токен для полужирного шрифта
        """
        return BoldToken(parser).getToken()


    @staticmethod
    def makeSection (parser):
        """
        Создать токен для раздела
        """
        return SectionToken(parser).getToken()


class FontToken (object):
    def __init__ (self, parser):
        self.parser = parser


    def convertToHTML (self, opening, closing):
        """
        opening - открывающийся тег(и)
        closing - закрывающийся тег(и)
        """
        def conversionParseAction (s, l, t):
            return u"".join ([opening, t["text"], closing])

        return conversionParseAction


class ItalicToken (FontToken):
    """
    Токен для курсива
    """
    def getToken (self):
        reg = r"\{\\it(\\\w+)?\s+(?P<text>.+?)\s*\}"

        return Regex (reg,
                      flags=re.M | re.S | re.I | re.U).setParseAction (
                          self.convertToHTML (u"<i>", u"</i>"))("italic")


class BoldToken (FontToken):
    """
    Токен для полужирного шрифта
    """
    def getToken (self):
        reg = r"\{\\bf(\\\w+)?\s+(?P<text>.+?)\s*\}"

        return Regex (reg,
                      flags=re.M | re.S | re.I | re.U).setParseAction (
                          self.convertToHTML (u"<b>", u"</b>"))("bold")


class SectionToken (FontToken):
    """
    Токен для заголовка раздела
    """
    def getToken (self):
        reg = r"\\section\{\s*(?P<text>.+?)\s*\}"

        return Regex (reg,
                      flags=re.M | re.S | re.I | re.U).setParseAction (
                          self.convertToHTML (u"<h2>", u"</h2>"))("section")

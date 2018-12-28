# -*- coding: utf-8 -*-

from outwiker.libs.pyparsing import Regex

from .tokenfonts import SubscriptToken, SuperscriptToken, BoldToken, ItalicToken, BoldItalicToken
from .utils import escapeTextForRE


class AdHocFactory(object):
    @staticmethod
    def makeBoldSubscript(parser):
        return BoldSubscriptToken(parser).getToken()

    @staticmethod
    def makeBoldSuperscript(parser):
        return BoldSuperscriptToken(parser).getToken()

    @staticmethod
    def makeItalicSubscript(parser):
        return ItalicSubscriptToken(parser).getToken()

    @staticmethod
    def makeItalicSuperscript(parser):
        return ItalicSuperscriptToken(parser).getToken()

    @staticmethod
    def makeBoldItalicSubscript(parser):
        return BoldItalicSubscriptToken(parser).getToken()

    @staticmethod
    def makeBoldItalicSuperscript(parser):
        return BoldItalicSuperscriptToken(parser).getToken()

    @staticmethod
    def make(parser):
        return(AdHocFactory.makeBoldItalicSubscript(parser) |
               AdHocFactory.makeBoldItalicSuperscript(parser) |
               AdHocFactory.makeBoldSubscript(parser) |
               AdHocFactory.makeBoldSuperscript(parser) |
               AdHocFactory.makeItalicSubscript(parser) |
               AdHocFactory.makeItalicSuperscript(parser)
               )


class AdHocToken(object):
    """
    Базовый класс для отдельных проблемных случаев при разборе вики-нотации
    """
    def __init__(self, parser):
        self.parser = parser

    def getDefaultToken(self, outerStart, outerEnd, innerStart, innerEnd):
        outerEnd_for_RE = escapeTextForRE(outerEnd)
        innerStart_for_RE = escapeTextForRE(innerStart)
        innerEnd_for_RE = escapeTextForRE(innerEnd)

        return (outerStart +
                Regex('(?:(?!' + outerEnd_for_RE + ').)*?' + innerStart_for_RE + '.*?' + innerEnd_for_RE) +
                outerEnd)

    def getAction(self, opening, closing):
        def conversionParseAction(s, l, t):
            return opening + self.parser.parseTextLevelMarkup(t[1]) + closing
        return conversionParseAction


class BoldSubscriptToken(AdHocToken):
    """
    Токен для полужирного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    BoldToken.start, BoldToken.end,
                    SubscriptToken.start, SubscriptToken.end)("bold_subscript")
        token.setParseAction(self.getAction(u'<b>', u'</b>'))
        return token


class BoldSuperscriptToken(AdHocToken):
    """
    Токен для полужирного верхнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    BoldToken.start, BoldToken.end,
                    SuperscriptToken.start, SuperscriptToken.end)("bold_superscript")

        token.setParseAction(self.getAction(u'<b>', u'</b>'))
        return token


class ItalicSubscriptToken(AdHocToken):
    """
    Токен для курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    ItalicToken.start, ItalicToken.end,
                    SubscriptToken.start, SubscriptToken.end)("italic_subscript")

        token.setParseAction(self.getAction(u'<i>', u'</i>'))
        return token


class ItalicSuperscriptToken(AdHocToken):
    """
    Токен для курсивного верхнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    ItalicToken.start, ItalicToken.end,
                    SuperscriptToken.start, SuperscriptToken.end)("italic_superscript")

        token.setParseAction(self.getAction(u'<i>', u'</i>'))
        return token


class BoldItalicSubscriptToken(AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    BoldItalicToken.start, BoldItalicToken.end,
                    SubscriptToken.start, SubscriptToken.end)("bold_italic_subscript")

        token.setParseAction(self.getAction(u'<b><i>', u'</i></b>'))
        return token


class BoldItalicSuperscriptToken(AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = self.getDefaultToken(
                    BoldItalicToken.start, BoldItalicToken.end,
                    SuperscriptToken.start, SuperscriptToken.end)("bold_italic_superscript")

        token.setParseAction(self.getAction(u'<b><i>', u'</i></b>'))
        return token

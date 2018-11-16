# -*- coding: utf-8 -*-

from outwiker.libs.pyparsing import Regex

from .tokenfonts import SubscriptToken, BoldToken, ItalicToken, BoldItalicToken


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
        token = (BoldToken.start +
                 Regex('.*?' + SubscriptToken.start + '.*?' + SubscriptToken.end) +
                 BoldToken.end)("bold_subscript")

        token.setParseAction(self.getAction(u'<b>', u'</b>'))
        return token


class BoldSuperscriptToken(AdHocToken):
    """
    Токен для полужирного верхнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = (BoldToken.start +
                 Regex(r".*?'\^.*?\^'") +
                 BoldToken.end)("bold_superscript")

        token.setParseAction(self.getAction(u'<b>', u'</b>'))
        return token


class ItalicSubscriptToken(AdHocToken):
    """
    Токен для курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = (ItalicToken.start +
                 Regex('.*?' + SubscriptToken.start + '.*?' + SubscriptToken.end) +
                 ItalicToken.end)("italic_subscript")

        token.setParseAction(self.getAction(u'<i>', u'</i>'))
        return token


class ItalicSuperscriptToken(AdHocToken):
    """
    Токен для курсивного верхнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = (ItalicToken.start +
                 Regex(r".*?'\^.*?\^'") +
                 ItalicToken.end)("italic_superscript")

        token.setParseAction(self.getAction(u'<i>', u'</i>'))
        return token


class BoldItalicSubscriptToken(AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = (BoldItalicToken.start +
                 Regex('.*?' + SubscriptToken.start + '.*?' + SubscriptToken.end) +
                 BoldItalicToken.end)("bold_italic_subscript")

        token.setParseAction(self.getAction(u'<b><i>', u'</i></b>'))
        return token


class BoldItalicSuperscriptToken(AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__(self, parser):
        AdHocToken.__init__(self, parser)

    def getToken(self):
        token = (BoldItalicToken.start +
                 Regex(r".*?'\^.*?\^'") +
                 BoldItalicToken.end)("bold_italic_superscript")

        token.setParseAction(self.getAction(u'<b><i>', u'</i></b>'))
        return token

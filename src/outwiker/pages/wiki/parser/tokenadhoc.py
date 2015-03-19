# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString

from tokenfonts import SubscriptToken, SuperscriptToken, BoldToken, ItalicToken, BoldItalicToken


class AdHocFactory (object):
    @staticmethod
    def makeBoldSubscript (parser):
        return BoldSubscriptToken(parser).getToken()


    @staticmethod
    def makeBoldSuperscript (parser):
        return BoldSuperscriptToken(parser).getToken()


    @staticmethod
    def makeItalicSubscript (parser):
        return ItalicSubscriptToken(parser).getToken()


    @staticmethod
    def makeItalicSuperscript (parser):
        return ItalicSuperscriptToken(parser).getToken()


    @staticmethod
    def makeBoldItalicSubscript (parser):
        return BoldItalicSubscriptToken(parser).getToken()


    @staticmethod
    def makeBoldItalicSuperscript (parser):
        return BoldItalicSuperscriptToken(parser).getToken()


    @staticmethod
    def make(parser):
        return (AdHocFactory.makeBoldItalicSubscript (parser) |
                AdHocFactory.makeBoldItalicSuperscript (parser) |
                AdHocFactory.makeBoldSubscript (parser) |
                AdHocFactory.makeBoldSuperscript (parser) |
                AdHocFactory.makeItalicSubscript (parser) |
                AdHocFactory.makeItalicSuperscript (parser)
                )



class AdHocToken (object):
    """
    Базовый класс для отдельных проблемных случаев при разборе вики-нотации
    """
    def __init__ (self, parser):
        self.parser = parser


    def convertToHTMLAdHoc(self, opening, closing, prefix=u"", suffix=u""):
        """
        Преобразование в HTML для отдельный случаев, когда надо добавить в начало или конец обрабатываемой строки префикс или суффикс
        """
        def conversionParseAction(s, l, t):
            return opening + self.parser.parseTextLevelMarkup (prefix + t[0] + suffix) + closing
        return conversionParseAction


class BoldSubscriptToken (AdHocToken):
    """
    Токен для полужирного нижнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldToken.boldStart,
                             endQuoteChar = SubscriptToken.subscriptEnd + BoldToken.boldEnd,
                             multiline = True).setParseAction(
                                 self.convertToHTMLAdHoc("<b>",
                                                         "</b>",
                                                         suffix = SubscriptToken.subscriptEnd))("bold_subscript")



class BoldSuperscriptToken (AdHocToken):
    """
    Токен для полужирного верхнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldToken.boldStart,
                             endQuoteChar = SuperscriptToken.superscriptEnd + BoldToken.boldEnd,
                             multiline = True).setParseAction (self.convertToHTMLAdHoc (
                                 "<b>",
                                 "</b>",
                                 suffix = SuperscriptToken.superscriptEnd))("bold_superscript")


class ItalicSubscriptToken (AdHocToken):
    """
    Токен для курсивного нижнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (ItalicToken.italicStart,
                             endQuoteChar = SubscriptToken.subscriptEnd + ItalicToken.italicEnd,
                             multiline = True).setParseAction(self.convertToHTMLAdHoc(
                                 "<i>",
                                 "</i>",
                                 suffix = SubscriptToken.subscriptEnd))("italic_subscript")



class ItalicSuperscriptToken (AdHocToken):
    """
    Токен для курсивного верхнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (ItalicToken.italicStart,
                             endQuoteChar = SuperscriptToken.superscriptEnd + ItalicToken.italicEnd,
                             multiline = True).setParseAction(self.convertToHTMLAdHoc(
                                 "<i>",
                                 "</i>",
                                 suffix = SuperscriptToken.superscriptEnd))("italic_superscript")


class BoldItalicSubscriptToken (AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldItalicToken.boldItalicStart,
                             endQuoteChar = SubscriptToken.subscriptEnd + BoldItalicToken.boldItalicEnd,
                             multiline = True).setParseAction(self.convertToHTMLAdHoc(
                                 "<b><i>",
                                 "</i></b>",
                                 suffix = SubscriptToken.subscriptEnd))("bold_italic_subscript")



class BoldItalicSuperscriptToken (AdHocToken):
    """
    Токен для полужирного курсивного нижнего индекса
    """
    def __init__ (self, parser):
        AdHocToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldItalicToken.boldItalicStart,
                             endQuoteChar = SuperscriptToken.superscriptEnd + BoldItalicToken.boldItalicEnd,
                             multiline = True).setParseAction(self.convertToHTMLAdHoc(
                                 "<b><i>",
                                 "</i></b>",
                                 suffix = SuperscriptToken.superscriptEnd))("bold_italic_superscript")

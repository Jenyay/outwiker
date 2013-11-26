#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import QuotedString, Regex

from tokenblock import BlockToken

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
    def makeBoldItalic (parser):
        """
        Создать токен для полужирного курсивного шрифта
        """
        return BoldItalicToken(parser).getToken()


    @staticmethod
    def makeUnderline (parser):
        """
        Создать токен для подчеркнутого шрифта
        """
        return UnderlineToken(parser).getToken()


    @staticmethod
    def makeStrike (parser):
        """
        Создать токен для зачеркнутого шрифта
        """
        return StrikeToken(parser).getToken()


    @staticmethod
    def makeSubscript (parser):
        """
        Создать токен для нижнего индекса
        """
        return SubscriptToken(parser).getToken()


    @staticmethod
    def makeSuperscript (parser):
        """
        Создать токен для верхнего индекса
        """
        return SuperscriptToken(parser).getToken()


    @staticmethod
    def makeCode (parser):
        """
        Создать токен для кода
        """
        return CodeToken(parser).getToken()


    @staticmethod
    def makeSmall (parser):
        """
        Создать парсер для мелкого шрифта
        """
        return SmallFontToken(parser).getToken()


    @staticmethod
    def makeBig (parser):
        """
        Создать парсер для крупного шрифта
        """
        return BigFontToken(parser).getToken()



class CodeToken (BlockToken):
    """
    Токен для кода
    """
    codeStart = "@@"
    codeEnd = "@@"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (CodeToken.codeStart, 
                endQuoteChar = CodeToken.codeEnd, 
                multiline = True).setParseAction(self.convertToHTML("<code>","</code>"))("code")


class SuperscriptToken (BlockToken):
    """
    Токен для верхнего индекса
    """
    superscriptStart = "'^"
    superscriptEnd = "^'"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (SuperscriptToken.superscriptStart, 
                endQuoteChar = SuperscriptToken.superscriptEnd, 
                multiline = True).setParseAction(self.convertToHTML("<sup>","</sup>"))("superscript")


class SubscriptToken (BlockToken):
    """
    Токен для нижнего индекса
    """
    subscriptStart = "'_"
    subscriptEnd = "_'"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (SubscriptToken.subscriptStart, 
                endQuoteChar = SubscriptToken.subscriptEnd, 
                multiline = True).setParseAction(self.convertToHTML("<sub>","</sub>"))("subscript")


class UnderlineToken (BlockToken):
    """
    Токен для курсива
    """
    underlineStart = "{+"
    underlineEnd = "+}"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (UnderlineToken.underlineStart, 
                endQuoteChar = UnderlineToken.underlineEnd, 
                multiline = True).setParseAction(self.convertToHTML("<u>","</u>"))("underline")


class StrikeToken (BlockToken):
    """
    Токен для курсива
    """
    strikeStart = "{-"
    strikeEnd = "-}"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (StrikeToken.strikeStart, 
                endQuoteChar = StrikeToken.strikeEnd, 
                multiline = True).setParseAction(self.convertToHTML("<strike>","</strike>"))("strike")



class ItalicToken (BlockToken):
    """
    Токен для курсива
    """
    italicStart = "''"
    italicEnd = "''"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (ItalicToken.italicStart, 
                endQuoteChar = ItalicToken.italicEnd, 
                multiline = True).setParseAction(self.convertToHTML("<i>","</i>"))("italic")
    

class BoldToken (BlockToken):
    """
    Токен для полужирного шрифта
    """
    boldStart = "'''"
    boldEnd = "'''"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldToken.boldStart, 
                endQuoteChar = BoldToken.boldEnd, 
                multiline = True).setParseAction(self.convertToHTML("<b>","</b>"))("bold")


class BoldItalicToken (BlockToken):
    """
    Токен для полужирного курсивного шрифта
    """
    boldItalicStart = "''''"
    boldItalicEnd = "''''"

    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return QuotedString (BoldItalicToken.boldItalicStart, 
                endQuoteChar = BoldItalicToken.boldItalicEnd, 
                multiline = True).setParseAction(self.convertToHTML("<b><i>","</i></b>"))("bold_italic")


class SmallFontToken (BlockToken):
    """
    Токен для мелкого шрифта
    """
    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return Regex (r"\[(?P<count>-{1,4})(?P<text>.*?)\1\]", re.MULTILINE | re.UNICODE | re.DOTALL).setParseAction (self.__parse)("small")


    def __parse (self, s, l, t):
        # Расчет масштаба в зависимости от количества минусов
        size = 100 - len (t["count"]) * 20

        return u'<span style="font-size:{size}%">{text}</span>'.format (size=size, text=self.parser.parseWikiMarkup (t["text"]))


class BigFontToken (BlockToken):
    """
    Токен для крупного шрифта
    """
    def __init__ (self, parser):
        BlockToken.__init__ (self, parser)


    def getToken (self):
        return Regex (r"\[(?P<count>\+{1,5})(?P<text>.*?)\1\]", re.MULTILINE | re.UNICODE | re.DOTALL).setParseAction (self.__parse)("big")


    def __parse (self, s, l, t):
        # Расчет масштаба в зависимости от количества минусов
        size = 100 + len (t["count"]) * 20

        return u'<span style="font-size:{size}%">{text}</span>'.format (size=size, text=self.parser.parseWikiMarkup (t["text"]))

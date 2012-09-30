#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString

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
                multiline = True).setParseAction(self.convertToHTML("<CODE>","</CODE>"))("code")


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
                multiline = True).setParseAction(self.convertToHTML("<SUP>","</SUP>"))("super")


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
                multiline = True).setParseAction(self.convertToHTML("<SUB>","</SUB>"))("subscript")


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
                multiline = True).setParseAction(self.convertToHTML("<U>","</U>"))("underline")


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
                multiline = True).setParseAction(self.convertToHTML("<STRIKE>","</STRIKE>"))("strike")



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
                multiline = True).setParseAction(self.convertToHTML("<I>","</I>"))("italic")
    

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
                multiline = True).setParseAction(self.convertToHTML("<B>","</B>"))("bold")


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
                multiline = True).setParseAction(self.convertToHTML("<B><I>","</I></B>"))("bold_italic")

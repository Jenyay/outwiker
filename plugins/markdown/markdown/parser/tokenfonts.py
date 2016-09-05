# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString


class FontsFactory(object):
    """
    Фабрика для создания шрифтовых / блочных токенов
    """
    @staticmethod
    def makeItalic():
        """
        Создать токен для курсивного шрифта
        """
        return ItalicToken().getToken()

    @staticmethod
    def makeBold():
        """
        Создать токен для полужирного шрифта
        """
        return BoldToken().getToken()

    @staticmethod
    def makeBoldItalic():
        """
        Создать токен для полужирного курсивного шрифта
        """
        return BoldItalicToken().getToken()


class ItalicToken (object):
    start_1 = "*"
    end_1 = "*"

    start_2 = "_"
    end_2 = "_"

    def getToken(self):
        return (QuotedString(ItalicToken.start_1,
                             endQuoteChar=ItalicToken.end_1,
                             multiline=True) |
                QuotedString(ItalicToken.start_2,
                             endQuoteChar=ItalicToken.end_2,
                             multiline=True))("italic")


class BoldToken(object):
    start_1 = "**"
    end_1 = "**"

    start_2 = "__"
    end_2 = "__"

    def getToken(self):
        return (QuotedString(BoldToken.start_1,
                             endQuoteChar=BoldToken.end_1,
                             multiline=True) |
                QuotedString(BoldToken.start_2,
                             endQuoteChar=BoldToken.end_2,
                             multiline=True))("bold")


class BoldItalicToken(object):
    start = "**_"
    end = "_**"

    def getToken(self):
        return QuotedString(BoldItalicToken.start,
                            endQuoteChar=BoldItalicToken.end,
                            multiline=True)("bold_italic")

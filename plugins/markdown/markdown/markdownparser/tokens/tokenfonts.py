# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString


class FontsFactory(object):
    """
    Фабрика для создания шрифтовых / блочных токенов
    """
    @staticmethod
    def makeItalic():
        """
        Create token for italic font
        """
        return ItalicToken().getToken()

    @staticmethod
    def makeBold():
        """
        Create token for bold font
        """
        return BoldToken().getToken()

    @staticmethod
    def makeBoldItalic():
        """
        Create token for bold italic font
        """
        return BoldItalicToken().getToken()

    @staticmethod
    def makeCode():
        """
        Create token for the code block
        """
        return CodeToken().getToken()


class BlockToken(object):
    def checkBreaks(self, s, loc, toks):
        text = toks[0].replace(u'\r\n', u'\n')
        return text.find(u'\n\n') == -1


class ItalicToken (BlockToken):
    start_1 = "*"
    end_1 = "*"

    start_2 = "_"
    end_2 = "_"

    def getToken(self):
        return (QuotedString(ItalicToken.start_1,
                             endQuoteChar=ItalicToken.end_1,
                             multiline=True,
                             convertWhitespaceEscapes=False) |
                QuotedString(ItalicToken.start_2,
                             endQuoteChar=ItalicToken.end_2,
                             multiline=True,
                             convertWhitespaceEscapes=False)).addCondition(self.checkBreaks)("italic")


class BoldToken(BlockToken):
    start_1 = "**"
    end_1 = "**"

    start_2 = "__"
    end_2 = "__"

    def getToken(self):
        return (QuotedString(BoldToken.start_1,
                             endQuoteChar=BoldToken.end_1,
                             multiline=True,
                             convertWhitespaceEscapes=False) |
                QuotedString(BoldToken.start_2,
                             endQuoteChar=BoldToken.end_2,
                             multiline=True,
                             convertWhitespaceEscapes=False)).addCondition(self.checkBreaks)("bold")


class BoldItalicToken(BlockToken):
    start = "**_"
    end = "_**"

    def getToken(self):
        return QuotedString(BoldItalicToken.start,
                            endQuoteChar=BoldItalicToken.end,
                            multiline=True,
                            convertWhitespaceEscapes=False).addCondition(self.checkBreaks)("bold_italic")


class CodeToken(BlockToken):
    start = "```"
    end = "```"

    def getToken(self):
        return QuotedString(CodeToken.start,
                            endQuoteChar=CodeToken.end,
                            multiline=True,
                            convertWhitespaceEscapes=False)("code")

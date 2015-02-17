# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Literal


class LineBreakFactory (object):
    @staticmethod
    def make (parser):
        return LineBreakToken().getToken()


class LineBreakToken (object):
    """
    Токен для горизонтальной линии
    """
    expression1 = "[[<<]]"
    expression2 = "[[&lt;&lt;]]"

    def getToken (self):
        token1 = Literal (LineBreakToken.expression1).setParseAction (lambda s, l, t: "<br/>")
        token2 = Literal (LineBreakToken.expression2).setParseAction (lambda s, l, t: "<br/>")
        return (token1 | token2)("linebreak")

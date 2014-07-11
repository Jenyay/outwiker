# -*- coding: UTF-8 -*-

import re

from ..libs.pyparsing import Regex


class TableFactory (object):
    """
    Фабрика для создания токена для разбора таблиц
    """
    @staticmethod
    def make (parser):
        """
        Создать токен для курсивного шрифта
        """
        return TableToken(parser).getToken()



class TableToken (object):
    """
    Токен для таблиц
    """
    def __init__ (self, parser):
        self._parser = parser


    def getToken (self):
        reg = r'''\\begin\{(?P<type>longtable|tabular)\}
        (?P<params>\{.*?\})\n
        (?P<body>.*?)
        \\end\{\1\}'''

        token = Regex (reg, flags=re.M | re.S | re.I | re.U | re.X)
        token.setParseAction (self._convertToHTML)

        return token


    def _convertToHTML (self, s, l, t):
        return u"".join ([u"<table border=1>", self._parseBody (t["body"]), "</table>"])


    def _parseBody (self, body):
        rows = [row.strip() for row in body.split (r"\\") if len (row.strip()) != 0]

        result = []
        for row in rows:
            result.append (u"<tr>")
            result.append (self._parseRow (row))
            result.append (u"</tr>")

        return u"".join (result)


    def _parseRow (self, row):
        cols = [col.strip() for col in row.split ("&")]

        result = []
        for col in cols:
            result.append (u"<td>")
            result.append (self._parser.convert (col))
            result.append (u"</td>")

        return u"".join (result)

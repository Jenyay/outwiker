#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart


class TableFactory (object):
    @staticmethod
    def make (parser):
        return TableToken(parser).getToken()


class TableToken (object):
    """
    Токен для таблиц
    """
    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        tableCell = Regex (r"(?P<text>(.|(\\\n))*?)(\\\n\s*)*\|\|", re.UNICODE)
        tableCell.setParseAction(self.__convertTableCell)

        tableRow = LineStart() + "||" + OneOrMore (tableCell) + Optional (LineEnd())
        tableRow.setParseAction(self.__convertTableRow)

        table = LineStart() + Regex (r"\|\| *(?P<params>.+)?", re.UNICODE) + LineEnd() + OneOrMore (tableRow)
        table = table.setParseAction(self.__convertTable)("table")

        return table


    def __convertTableCell (self, s, loc, toks):
        text = toks["text"]

        leftAlign = toks["text"][-1] in " \t"
        
        # Условие в скобках связано с тем, что первый пробел попадает 
        # или не попадает в токен в зависимости от того, первая ячейка в строке или нет
        rightAlign = loc > 0 and (s[loc - 1] in " \t" or s[loc] in " \t")

        align = u''

        if leftAlign and rightAlign:
            align = u' align="center"'
        elif leftAlign:
            align = u' align="left"'
        elif rightAlign:
            align = u' align="right"'

        result = u'<td%s>%s</td>' % (align, self.parser.parseWikiMarkup (text.strip() ) )

        return result


    def __convertTableRow (self, s, l, t):
        if t[-1] == "\n":
            lastindex = len (t) - 1
        else:
            lastindex = len (t)

        result = u"<tr>"
        for element in t[1: lastindex]:
            result += element

        result += "</tr>"

        return result


    def __convertTable (self, s, l, t):
        result = u"<table %s>" % t[0][2:].strip()
        for element in t[2:]:
            result += element

        result += "</table>"

        return result

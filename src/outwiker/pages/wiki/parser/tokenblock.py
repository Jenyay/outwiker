#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class BlockToken (object):
    """
    Класс, содержащий метод для оборачивания текста в блочные теги
    """
    def __init__ (self, parser):
        self.parser = parser


    def convertToHTML (self, opening, closing):
        """
        opening - открывающийся тег(и)
        closing - закрывающийся тег(и)
        """
        def conversionParseAction(s,l,t):
            return opening + self.parser.parseWikiMarkup (t[0]) + closing
        return conversionParseAction

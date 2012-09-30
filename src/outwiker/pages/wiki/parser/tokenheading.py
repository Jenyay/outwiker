#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class HeadingFactory (object):
    @staticmethod
    def make (parser):
        return HeadingToken(parser).getToken()


class HeadingToken (object):
    def __init__ (self, parser):
        self.heading_Regex = "^(?P<header>!!+)\s+(?P<title>.*)$"
        self.parser = parser


    def getToken (self):
        """
        Токены для заголовков H1, H2,...
        """
        return Regex (self.heading_Regex, re.MULTILINE).setParseAction(self.convertToHeading)("heading")


    def convertToHeading (self, s, l, t):
        level = len (t["header"]) - 1
        content = self.parser.parseHeadingMarkup (t["title"])
        return u"<H{level}>{content}</H{level}>".format (level=level, content=content)

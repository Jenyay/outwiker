# -*- coding: utf-8 -*-

import re

from pyparsing import Regex

import outwiker.core.cssclasses as css


class HeadingFactory:
    @staticmethod
    def make(parser):
        return HeadingToken(parser).getToken()


class HeadingToken:
    def __init__(self, parser):
        self.heading_Regex = r"^(?P<header>!!+)\s+(?P<title>(\\\n|.)*)$"
        self.parser = parser

    def getToken(self):
        """
        Токены для заголовков H1, H2,...
        """
        return Regex(self.heading_Regex, re.MULTILINE).setParseAction(self.convertToHeading)("heading")

    def convertToHeading(self, s, l, t):
        level = len(t["header"]) - 1
        content = self.parser.parseHeadingMarkup(t["title"])
        return '<h{level} class="{css_class}">{content}</h{level}>'.format(level=level, content=content, css_class=css.CSS_WIKI)

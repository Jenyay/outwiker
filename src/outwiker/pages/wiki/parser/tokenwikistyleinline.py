# -*- coding: utf-8 -*-

from outwiker.libs.pyparsing import Regex, Forward, ZeroOrMore, OneOrMore, CharsNotIn, Literal, SkipTo, Suppress, originalTextFor, NotAny

from .tokennoformat import NoFormatFactory


class WikiStyleInlineFactory(object):
    """
    The fabric to create inline wiki style tokens.
    """
    @staticmethod
    def make(parser):
        return WikiStyleInline(parser).getToken()


class WikiStyleInline(object):
    start_html = ''
    end_html = '</span>'
    name = 'wikistyle_inline'

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        start = Regex(r'%\s*(?P<params>[\w\s."\'_=-]+?)\s*%')
        end = Literal('%%')

        token = Forward()
        no_format = NoFormatFactory.make(self.parser)

        before_end = SkipTo(no_format, failOn=end, ignore=no_format)
        nested_tokens = ZeroOrMore(SkipTo(token, failOn=end, ignore=no_format) + token)

        inside = originalTextFor(nested_tokens + before_end + SkipTo(end)).leaveWhitespace()
        token << start + inside + end

        token = token.setParseAction(self.conversionParseAction)(self.name)

        return token

    def conversionParseAction(self, s, l, t):
        # print()
        # print(s)
        # print(t)
        # print(t['params'])
        # print(t[1])
        class_name = t['params']
        inside = self.parser.parseWikiMarkup(t[1])

        result = '<span class="{class_name}">{inside}</span>'.format(
            class_name=class_name,
            inside=inside
        )

        # print(result)
        return result

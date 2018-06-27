# -*- coding: utf-8 -*-

import re

from outwiker.libs.pyparsing import (Regex, Forward, ZeroOrMore, Literal,
                                     SkipTo, originalTextFor)

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
        start = Regex(r'%\s*(?P<params>[\w\s."\'_=:;#()-]+?)\s*%')
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
        params_list = self._parseParams(t['params'])
        inside = self.parser.parseWikiMarkup(t[1])

        classes = []
        for param, value in params_list:
            if not value:
                classes.append(param)

        classes_str = ' class="' + ' '.join(classes) + '"' if classes else ''

        result = '<span{classes}>{inside}</span>'.format(
            classes=classes_str,
            inside=inside
        )

        return result

    def _parseParams(self, params):
        """
        Parse params string into parts: key - value. Key may contain a dot.
        Sample params:
            param1 Параметр2.subparam = 111 Параметр3 = " bla bla bla" param4.sub.param2 = "111" param5 =' 222 ' param7 = " sample 'bla bla bla' example" param8 = ' test "bla-bla-bla" test '
        """
        pattern = r"""((?P<name>#?[\w.-]+)(\s*=\s*(?P<param>([-_\w.]+)|((?P<quote>["']).*?(?P=quote)) ) )?\s*)"""

        result = []

        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        matches = regex.finditer(params)

        for match in matches:
            name = match.group("name")
            param = match.group("param")
            if param is None:
                param = u""

            result.append((name, self._removeQuotes(param)))

        return result

    def _removeQuotes(self, text):
        """
        Удалить начальные и конечные кавычки, которые остались после разбора параметров
        """
        if (len(text) > 0 and
                (text[0] == text[-1] == "'" or text[0] == text[-1] == '"')):
            return text[1:-1]

        return text

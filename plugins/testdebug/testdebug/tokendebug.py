# -*- coding: utf-8 -*-

from pyparsing import QuotedString

from outwiker.api.pages.wiki.wikiparser import TextBlockToken


class DebugTokenFactory:
    @staticmethod
    def makeDebugToken(parser):
        return DebugToken(parser).getToken()


class DebugToken(TextBlockToken):
    start = "{{{{"
    end = "}}}}"

    def getToken(self):
        return QuotedString(
            DebugToken.start,
            end_quote_char=DebugToken.end,
            multiline=True,
            convert_whitespace_escapes=False,
        ).set_parse_action(self.convertToHTML("<font color='red'>", "</font>"))("debug")

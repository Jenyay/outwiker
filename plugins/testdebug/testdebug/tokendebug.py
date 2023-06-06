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
            endQuoteChar=DebugToken.end,
            multiline=True,
            convertWhitespaceEscapes=False,
        ).setParseAction(self.convertToHTML("<font color='red'>", "</font>"))("debug")
